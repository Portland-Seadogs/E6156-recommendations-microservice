from application_services.base_application_resource import BaseApplicationResource, BaseApplicationException
import middleware.context as context
from flask import g
import asyncio
import requests


class ArtRecommendationException(BaseApplicationException):
    def __init__(self, msg=None):
        self.msg = msg


class ArtRecommendationResource(BaseApplicationResource):

    products_service = "products"
    orders_service = "orders"

    def __init__(self):
        super().__init__()
        self.service_urls = context.get_atomic_microservice_urls()

    def get_synchronous_recommendation(self, limit):
        # get the top popular orders
        # get items already purchased by user
        # recommend any items not already purchased within limit

        url = self.service_urls[self.orders_service]
        headers = {"Authorization": g.access_token}  # use users access token
        r = requests.get(url=url, headers=headers)

    def get_synchronous_purchase_history(self, user_id):
        base_url = self.service_urls[self.orders_service]
        endpoint = ""
        headers = {"Authorization": g.access_token}  # use users access token
        return requests.get(url=base_url + endpoint, headers=headers)

    @classmethod
    def get_recommendation(cls, limit):

        # get the top popular orders
        # get items already purchased by user
        # recommend any items not already purchased within limit

        headers = {"Authorization": g.access_token}  # use users access token

