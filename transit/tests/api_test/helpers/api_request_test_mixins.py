from typing import Dict, Any, Optional

import django.db.models
from rest_framework import status

from transit.tests.api_test.helpers.api_crud_test_case import ModelViewsetRequestTestBase


class GetRequestTestMixin(ModelViewsetRequestTestBase):
    EXPECTED_GET_STATUS = status.HTTP_200_OK

    def test_get_list(self):
        response = self.get_request_result()
        self.assertEqual(response.status_code, self.EXPECTED_GET_STATUS, F"Response detail: {response.data}")
        self.assertTrue(len(response.data) > 0)

    def test_get_unique(self):
        response = self.get_request_result(detail=True)
        self.assertEqual(response.status_code, self.EXPECTED_GET_STATUS, F"Response detail: {response.data}")
        for payload_property, payload_value in self.expected_get_payload_properties.items():
            self.assertEqual(payload_value, response.data.get(payload_property, None))

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        raise NotImplementedError()


class PostRequestTestMixin(ModelViewsetRequestTestBase):
    EXPECTED_POST_STATUS = status.HTTP_201_CREATED

    def test_post(self):
        response = self.post_request_result()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, F"Response detail: {response.data}")
        created = self.expected_post_obj
        self.assertIsNotNone(created)

    @property
    def expected_post_obj(self) -> Optional[django.db.models.Model]:
        raise NotImplementedError()


class PatchRequestTestMixin(ModelViewsetRequestTestBase):
    EXPECTED_PATCH_STATUS = status.HTTP_200_OK

    def test_patch(self):
        response = self.patch_request_result()
        self.assertEqual(response.status_code, status.HTTP_200_OK, F"Response detail: {response.data}")
        updated = self.expected_patch_obj
        self.assertIsNotNone(updated)

    @property
    def expected_patch_obj(self) -> Optional[django.db.models.Model]:
        raise NotImplementedError()


class DeleteRequestTestMixin(ModelViewsetRequestTestBase):
    EXPECTED_DELETE_STATUS = status.HTTP_204_NO_CONTENT

    def test_delete(self):
        response = self.delete_request()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, F"Response detail: {response.data}")
        obj = self.expected_deleted_obj
        self.assertIsNone(obj)

    @property
    def expected_deleted_obj(self) -> Optional[django.db.models.Model]:
        raise NotImplementedError()
