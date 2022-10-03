from typing import Dict, Any

from django.test import TestCase

from transit.models import Item
from transit.rest_api.forms.item_master import ItemViewSet
from transit.tests.api_test.helpers.api_manual_form_test_case import ManualFormTestCaseMixin
from transit.tests.test_objects_factory import ItemFactory


class TestItemViewSet(ManualFormTestCaseMixin, TestCase):
    _URL = 'item'
    _VIEW_SET = ItemViewSet
    _MODEL_TYPE = Item

    _TEST_SUBJECT_DATA = ItemFactory.default_values.copy()
    _POST_REQUEST_PAYLOAD = {
        **ItemFactory.default_values.copy(), 'name': 'TestItemNew', 'volume': '30.20'}
    _PATCH_REQUEST_PAYLOAD = {'name': 'UpdatedField', 'conditions': 'Ambient', 'cost': '12.05'}

    @property
    def expected_get_payload_properties(self) -> Dict[str, Any]:
        return {
            'name': "ItemName", 'volume': '20.000000', 'cost': '40.00',
            'weight': '50.000000', 'category': 'ItemCategory',
            'sub_category': 'SubCategory', 'conditions': 'ColdChain'
        }
