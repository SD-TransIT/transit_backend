from typing import Dict, Any

from django.test import TestCase

from transit.models import ItemDetails
from transit.rest_api.manual_uploads.item_details import ItemDetailsViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.api_test.helpers.test_objects_factory import ItemDetailsFactory, ItemFactory


class TestItemDetailsViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'item_details'
    _VIEW_SET = ItemDetailsViewSet
    _MODEL_TYPE = ItemDetails
    _TEST_SUBJECT_DATA = ItemDetailsFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        **ItemDetailsFactory.default_values.copy(), 'gtin': 11111, 'funding_source': 'PostFundingSource',
    }
    _PATCH_REQUEST_PAYLOAD = {'batch_number': 'UpdatedBatch', 'funding_source': 'PatchFundingSource'}

    @classmethod
    def _get_or_create_test_subject(cls):
        return ItemDetailsFactory().create_object(True)

    def setUp(self):
        super(TestItemDetailsViewSet, self).setUp()
        self._additional_item = ItemFactory(custom_props={"name": "SecondItem"}).create_object(save=True)
        self._PATCH_REQUEST_PAYLOAD['item'] = self._additional_item.pk
        self._POST_REQUEST_PAYLOAD['item'] = self._additional_item.pk

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            'item': self.test_subject.item.pk, 'gtin': 9999999, 'batch_number': "ItemDetailsBatch",
            'lot_number': "ItemDetailLot", 'serial_number': "ItemDetailSerial",
            'funding_source': "ItemDetailFundingSource"
        }
