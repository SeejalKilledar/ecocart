from django.test import TestCase
from django.urls import reverse


class DashboardSmokeTests(TestCase):
    """Basic smoke tests to confirm the site boots and core pages load.

    These exist mainly so the CI pipeline has something real to run.
    Replace/expand with proper unit tests for your app logic.
    """

    def test_dashboard_page_loads(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_route_optimizer_page_loads(self):
        response = self.client.get(reverse('route_optimizer'))
        self.assertEqual(response.status_code, 200)

    def test_inventory_page_loads(self):
        response = self.client.get(reverse('inventory'))
        self.assertEqual(response.status_code, 200)

    def test_customer_segment_page_loads(self):
        response = self.client.get(reverse('customer_segment'))
        self.assertEqual(response.status_code, 200)

    def test_admin_login_page_loads(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)
