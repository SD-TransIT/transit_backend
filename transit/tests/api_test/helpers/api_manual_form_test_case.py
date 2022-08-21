from abc import ABC
from typing import Optional

from django.db import models

from transit.tests.api_test.helpers.api_request_test_mixins import GetRequestTestMixin, PostRequestTestMixin, \
    PatchRequestTestMixin, DeleteRequestTestMixin


class ManualFormTestCaseMixin(ABC, GetRequestTestMixin, PostRequestTestMixin,
                              PatchRequestTestMixin, DeleteRequestTestMixin):
    _USERNAME = 'FormsApiUser'

    def setUp(self):
        super(ManualFormTestCaseMixin, self).setUp()
        self.setup_helper()

    @property
    def expected_post_obj(self) -> Optional[models.Model]:
        return self._MODEL_TYPE.objects.filter(
            **self._POST_REQUEST_PAYLOAD
        ).first()

    @property
    def expected_patch_obj(self) -> Optional[models.Model]:
        return self._MODEL_TYPE.objects.filter(
            **self._PATCH_REQUEST_PAYLOAD, pk=self.test_subject.pk).first()

    @property
    def expected_deleted_obj(self) -> Optional[models.Model]:
        return self._MODEL_TYPE.objects.filter(pk=self.test_subject.pk).first()
