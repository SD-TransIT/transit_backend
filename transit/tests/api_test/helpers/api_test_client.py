from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class ApiTestClient:
    NAMESPACE = 'API'
    FORMAT = 'json'
    LOOKUP_KWARG = 'pk'
    _REVERSE_URL_BUILDER = {
        'get': lambda url, id_: reverse(F"API:{url}-detail", args=[id_]) if id_ else reverse(F"API:{url}-list"),
        'post': lambda url: reverse(F"API:{url}-list"),
        'patch': lambda url, id_: reverse(F"API:{url}-detail", kwargs={'pk': id_}),
        'delete': lambda url, id_: reverse(F"API:{url}-detail", kwargs={'pk': id_})
    }

    def __init__(self, endpoint_url, view):
        self._URL = endpoint_url
        self.factory = APIClient()
        self.view = view

    def make_get_request(self, identifier=None, auth_token=None):
        self._auth(auth_token)
        url = self._get_request_url('get', id_=identifier)
        return self.__make_request(self.factory.get, path=url)

    def make_post_request(self, payload, auth_token=None):
        self._auth(auth_token)
        url = self._get_request_url('post')
        return self.__make_request(self.factory.post, path=url, data=payload)

    def make_patch_request(self, payload, identifier, auth_token=None):
        self._auth(auth_token)
        url = self._get_request_url('patch', id_=identifier)
        return self.__make_request(self.factory.patch, path=url, data=payload)

    def make_delete_request(self, identifier, auth_token=None):
        url = self._get_request_url('delete', id_=identifier)
        self._auth(auth_token)
        return self.__make_request(self.factory.delete, path=url, data={'pk': identifier})

    def _get_request_url(self, method, **params):
        return self._REVERSE_URL_BUILDER[method](self._URL, **params)

    def __make_request(self, method, **data):
        if 'format' not in data.keys():
            data['format'] = 'json'
        return method(**data)

    def _auth(self, auth_token):
        if auth_token:
            self.factory.credentials(HTTP_AUTHORIZATION=auth_token)
        else:
            self.factory.credentials()


class TokenApiTestClient(ApiTestClient):
    _REVERSE_URL_BUILDER = {
        'get': lambda url, id_: reverse(F"transit-{url}"),
        'post': lambda url: reverse(F"{url}"),
        'patch': lambda url, id_: reverse(F"API:{url}", kwargs={'pk': id_}),
        'delete': lambda url, id_: reverse(F"API:{url}", kwargs={'pk': id_})
    }


class DeliveryStatusTestClient(ApiTestClient):
    # Has custom primary key - delivery_status_key
    _REVERSE_URL_BUILDER = {
        'get': lambda url, id_: reverse(F"API:{url}-detail", args=[id_]) if id_ else reverse(F"API:{url}-list"),
        'post': lambda url: reverse(F"API:{url}-list"),
        'patch': lambda url, id_: reverse(F"API:{url}-detail", kwargs={'delivery_status_key': id_}),
        'delete': lambda url, id_: reverse(F"API:{url}-detail", kwargs={'delivery_status_key': id_})
    }
