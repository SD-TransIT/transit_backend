from django.test import TestCase, RequestFactory

from transit.rest_api.authentication.jwt_views import DecoratedTokenObtainPairView
from transit.tests.api_test.mixin import UserMixin


class ApiTest(TestCase, UserMixin):
    _GET_ACTION = {'get': 'list'}
    _POST_ACTION = {'post': 'create'}
    _PUT_ACTION = {'put': 'update'}
    _DELETE_ACTION = {'delete': 'destroy'}

    def setUp(self):
        self.factory = RequestFactory(content_type='application/json')
        self.user = self.get_or_create_user()
        self.view = self.get_view()
        self.header = {"Content-Type": "application/json"}

    def get_view(self):
        raise NotImplementedError()

    def get_authorize_header(self, payload):
        request = self.factory.post('/token/', payload, **self.header)
        response = DecoratedTokenObtainPairView.as_view()(request)
        response_json = response.data
        return {
            "Content-Type": "application/json",
            "HTTP_AUTHORIZATION": f'Bearer {response_json["access"]}'
        }

    def make_get_request(self, endpoint, payload, actions=None):
        request = self.factory.get(endpoint, payload, **self.header)
        return self.__make_request(request, actions)

    def make_post_request(self, endpoint, payload, actions=None):
        request = self.factory.post(endpoint, payload, **self.header)
        return self.__make_request(request, actions)

    def make_put_request(self, endpoint, payload, identifier, actions=None):
        request = self.factory.put(endpoint, payload, content_type='application/json', **self.header)
        return self.__make_request(request, actions, identifier)

    def make_delete_request(self, endpoint, identifier, actions=None):
        request = self.factory.delete(endpoint, **self.header)
        return self.__make_request(request, actions, identifier)

    def __make_request(self, request, actions, identifier=None):
        if actions:
            return self.view.as_view(actions)(request, pk=identifier) \
                if identifier else self.view.as_view(actions)(request)
        else:
            return self.view.as_view()(request)
