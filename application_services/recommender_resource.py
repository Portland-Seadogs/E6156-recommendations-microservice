from gevent import monkey
monkey.patch_all()  # required change for bug in gevent/grequests combo
from application_services.base_application_resource import (
    BaseApplicationResource,
    BaseApplicationException,
)
import middleware.context as context
from flask import g
import random
import requests
import grequests


class ArtRecommendationException(BaseApplicationException):
    def __init__(self, msg=None):
        self.msg = msg


class RequestService:
    orders_service = "orders"
    products_service = "products"
    user_service = "users"

    @classmethod
    def user_info_url(cls):
        base_url = context.get_atomic_microservice_url(service=cls.user_service)
        endpoint = f"/users?googleID={g.google_user_id}"
        return base_url + endpoint

    @classmethod
    def user_orders_url(cls, user_id):
        base_url = context.get_atomic_microservice_url(service=cls.orders_service)
        endpoint = f"/orders/?user={user_id}"
        return base_url + endpoint

    @classmethod
    def full_catalog_url(cls):
        base_url = context.get_atomic_microservice_url(service=cls.products_service)
        endpoint = f"/catalog"
        return base_url + endpoint

    @classmethod
    def get_request_headers(cls):
        return {"Authorization": f"Bearer {g.access_token}"}


class ArtRecommendationResource(BaseApplicationResource):
    @classmethod
    def get_synchronous_recommendation(cls, limit):
        headers = RequestService.get_request_headers()
        user_id = cls._get_user_id(headers)
        purchase_history = (
            cls._get_synchronous_purchase_history(user_id, headers) if user_id else []
        )
        catalog = cls._get_synchronous_catalog(headers)
        return cls._extract_recommendations(purchase_history, catalog, limit)

    @classmethod
    def get_asynchronous_recommendation(cls, limit):
        headers = RequestService.get_request_headers()
        user_id = cls._get_user_id(headers)
        catalog_url = RequestService.full_catalog_url()
        orders_url = RequestService.user_orders_url(user_id)

        tasks = [
            grequests.get(catalog_url, headers=headers),
            grequests.get(orders_url, headers=headers),
        ]
        responses = grequests.map(tasks)
        if any(response.status_code != 200 for response in responses):
            return []

        # process result
        catalog, history = [result.json() for result in responses]
        purchase_history = cls._parse_user_item_id_history(history)
        return cls._extract_recommendations(purchase_history, catalog, limit)

    @classmethod
    def _extract_recommendations(cls, purchase_history, catalog, limit):
        """
        Makes recommendation based on user purchase history and catalog of available items.
        Limits results to the number provided as limit. For now, recommendations are
        made randomly from the set of items that the user has not already purchased.
        :return: List of products recommended
        """
        recommendations = []
        while len(recommendations) < limit and len(catalog):
            random_idx = random.randint(0, len(catalog) - 1)
            random_selection = catalog[random_idx]
            if random_selection["item_id"] not in purchase_history:
                recommendations.append(random_selection)
            catalog.pop(random_idx)
        return recommendations

    @classmethod
    def _get_user_id(cls, headers):
        """
        Finds the application user identifier based on the google auth ID
        :return: integer representing user ID in database, or None if could not be found
        """
        url = RequestService.user_info_url()
        resp = requests.get(url, headers=headers)
        resp_body = resp.json()
        if resp.status_code == 200 and resp_body:
            return resp_body[0]["ID"]
        return None

    @classmethod
    def _get_synchronous_purchase_history(cls, user_id, headers):
        """
        Get a set of all item ids previously purchased by a user
        :return: Set containing distinct item ids previously purchased
        """
        url = RequestService.user_orders_url(user_id)
        resp = requests.get(url, headers=headers)

        resp_body = resp.json()
        if resp.status_code != 200 or not resp_body:
            return set()
        return cls._parse_user_item_id_history(resp_body)

    @classmethod
    def _parse_user_item_id_history(cls, response_body):
        """
        Parse out all item ids purchased by user from request body
        :return: Set containing distinct item ids previously purchased
        """
        previously_purchased = set()
        for order in response_body["result"]["orders"]:
            for item in order["items"]:
                previously_purchased.add(item["item_id"])
        return previously_purchased

    @classmethod
    def _get_synchronous_catalog(cls, headers):
        """
        Get the full catalog of items
        :return: Contents of catalog, as dictionary
        """
        url = RequestService.full_catalog_url()
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            return []
        return resp.json()
