import os


class EnvironmentVarMissingException(BaseException):
    def __init__(self, msg):
        self.msg = msg


def get_atomic_microservice_urls():

    orders_url = os.environ.get("ORDERS_URL", None)
    products_url = os.environ.get("PRODUCTS_URL", None)
    users_url = os.environ.get("USERS_ADDRESSES_URL", None)

    if any(url is None for url in [orders_url, products_url, users_url]):
        raise EnvironmentVarMissingException("Ensure that ORDERS_URL, PRODUCTS_URL, and \\ "
                                             "USER_ADDRESSES_URL environmental vars are set.")

    return {
        'orders': orders_url,
        'products': products_url,
        'users': users_url
    }
