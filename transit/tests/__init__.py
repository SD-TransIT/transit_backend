from django.test import TestCase


class MockTestCase(TestCase):
    """
    Created to validate tests configuration. Remove after any actual test are added.
    """
    def test_true(self):
        self.assertTrue(True)
