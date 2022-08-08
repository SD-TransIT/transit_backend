from django.test import TestCase


class MockTestCase(TestCase):
    """
    Created to validate tests configuration and automatic builds. Remove after any actual test are added.
    """
    def test_true(self):
        self.assertTrue(True)

    def test_functionality_coverage(self):
        from transit.urls import urlpatterns  # noqa: WPS131
        self.assertGreater(len(urlpatterns), 1)

    def test_functionality_coverage3(self):
        from transit.urls import urlpatterns  # noqa: WPS131
        self.assertGreater(len(urlpatterns), 1)

    def test_functionality_coverage_2(self):
        from transit.rest_api import swagger_urls  # noqa: WPS131
        self.assertTrue(swagger_urls.schema_view is not None)
