from django.test import TestCase


class MockTestCase(TestCase):
    """
    Created to validate tests configuration and automatic builds. Remove after any actual test are added.
    """
    def test_true(self):
        self.assertTrue(True)

    def test_functionality_coverage(self):
        from transit.urls import urlpatterns
        self.assertGreater(len(urlpatterns), 1)
