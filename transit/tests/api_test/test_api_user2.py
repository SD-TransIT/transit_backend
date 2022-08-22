from typing import Dict, Any

from django.contrib.auth.models import User
from django.test import TestCase

from transit.rest_api.urls import UserViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin


class TestUserViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'users'
    _VIEW_SET = UserViewSet
    _MODEL_TYPE = User

    _TEST_SUBJECT_DATA = {
        'username': "StoredUser",
        'password': "P!@&EH2nod",
        'is_staff': True,
        'email': 'tesomas@sdo.sd'
    }

    _POST_REQUEST_PAYLOAD = {
        'username': "NewUser",
        'password': "P!@&EH2nod",
        'is_staff': True
    }

    _PATCH_REQUEST_PAYLOAD = {'username': "UpdatedUser"}

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            'username': "StoredUser",
            'id': self.test_subject.pk,
            'is_staff': True
        }

    @property
    def expected_post_obj(self):
        return self._MODEL_TYPE.objects.filter(username="NewUser", is_staff=True).first()
