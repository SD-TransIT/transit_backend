from dataclasses import dataclass
from typing import List, Dict, Type, Any

import django.db.models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from transit.models.user_proxy import MANAGE_USER_PERM, MANAGE_FORM_PERM
from transit.tests.api_test.helpers import UserTestHelper
from transit.tests.api_test.helpers.api_test_client import ApiTestClient


@dataclass
class ExpectedStatuses:
    get: int
    post: int
    patch: int
    delete: int


_FORBIDDEN = status.HTTP_403_FORBIDDEN
_UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED


class ViewSetRequestTestBase:
    _USERNAME: str = 'ApiAdminUser'
    _USER_PERMISSIONS: List[str] = [MANAGE_USER_PERM, MANAGE_FORM_PERM]
    _API_HELPER_TYPE: Type[ApiTestClient] = ApiTestClient

    _URL: str = ''
    _VIEW_SET: ModelViewSet = None
    _DETAIL_IDENTIFIER: Any

    _POST_REQUEST_PAYLOAD: Dict = {}  # Used in POST request
    _PATCH_REQUEST_PAYLOAD: Dict = {}  # Used in PATCH request

    @classmethod
    def setup_helper(cls):
        cls.API_HELPER = cls._API_HELPER_TYPE(cls._URL, cls._VIEW_SET)
        user_helper = UserTestHelper(username=cls._USERNAME)
        for permission in cls._USER_PERMISSIONS:
            user_helper.add_user_permission(permission)
        cls.USER_HELPER = user_helper

    def get_request_result(self, detail=False) -> Response:
        user_token = self.USER_HELPER.get_access_token()
        if detail:
            return self.API_HELPER.make_get_request(auth_token=user_token, identifier=self._DETAIL_IDENTIFIER)
        return self.API_HELPER.make_get_request(auth_token=user_token)

    def post_request_result(self) -> Response:
        user_token = self.USER_HELPER.get_access_token()
        return self.API_HELPER.make_post_request(self._POST_REQUEST_PAYLOAD, user_token)

    def patch_request_result(self) -> Response:
        user_token = self.USER_HELPER.get_access_token()
        return self.API_HELPER.make_patch_request(self._PATCH_REQUEST_PAYLOAD, self._DETAIL_IDENTIFIER, user_token)

    def delete_request(self) -> Response:
        user_token = self.USER_HELPER.get_access_token()
        return self.API_HELPER.make_delete_request(self._DETAIL_IDENTIFIER, user_token)


class ModelViewsetRequestTestBase(ViewSetRequestTestBase):
    _MODEL_TYPE: django.db.models.Model = None
    _TEST_SUBJECT_DATA: Dict = {}

    @classmethod
    def setup_helper(cls):
        super(ModelViewsetRequestTestBase, cls).setup_helper()
        test_subject = cls._get_or_create_test_subject()
        cls.test_subject = test_subject
        cls._DETAIL_IDENTIFIER = test_subject.pk

    @classmethod
    def _get_or_create_test_subject(cls):
        return cls._MODEL_TYPE.objects.create(**cls._TEST_SUBJECT_DATA)
