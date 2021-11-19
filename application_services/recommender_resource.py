from application_services.base_application_resource import BaseApplicationResource, BaseApplicationException
import middleware.context as context
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

    @classmethod
    def get_synchronous_recommendation(cls, limit):
        # get the top popular orders
        # get items already purchased by user
        # recommend any items not already purchased within limit
        pass

    @classmethod
    def get_recommendation(cls, limit):

        # get the top popular orders
        # get items already purchased by user
        # recommend any items not already purchased within limit
        pass


