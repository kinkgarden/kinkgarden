from django.test import TestCase, Client
from django.urls import reverse


class RTAMiddlewareTests(TestCase):
    def test_index_has_rta_header(self):
        response = self.client.get("/")
        self.assertEqual(response["Rating"], "RTA-5042-1996-1400-1577-RTA")


class AgeGateMiddlewareTests(TestCase):
    def test_index_shows_age_gate(self):
        client = Client()
        response = client.get("/")
        self.assertTemplateUsed(response, "base/age-gate.html")

    def test_non_index_shows_age_gate(self):
        client = Client()
        response = client.get(reverse("kinks:kink_list_new"))
        self.assertTemplateUsed(response, "base/age-gate.html")

    def test_privacy_policy_skips_age_gate(self):
        client = Client()
        response = client.get(reverse("base:privacy-policy"))
        self.assertTemplateUsed(response, "base/privacy_policy.html")

    def test_age_gate_accept_removes_persistently(self):
        client = Client()
        response = client.get("/")
        self.assertContains(
            response,
            '<input type="submit" name="age-gate-accept" value="Proceed">',
            html=True,
        )
        response = client.post("/", {"age-gate-accept": "Proceed"})
        self.assertTemplateNotUsed(response, "base/age-gate.html")
        response = client.get("/")
        self.assertTemplateNotUsed(response, "base/age-gate.html")

    def test_age_gate_reject_goes_offsite(self):
        client = Client()
        response = client.get("/")
        self.assertContains(
            response,
            '<input type="submit" name="age-gate-reject" value="Exit">',
            html=True,
        )
        response = client.post("/", {"age-gate-reject": "Exit"})
        self.assertRedirects(
            response, "https://example.com", fetch_redirect_response=False
        )


def approve_age_gate(client: Client):
    client.post("/", {"age-gate-accept": "Proceed"})
