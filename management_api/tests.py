from time import time
from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework.reverse import reverse
from rest_framework_simplejwt.backends import TokenBackend
import json

VALID_TOKEN_PAYLOAD = {
    "iss": "https://my-domain.us.auth0.com/",
    "sub": "user@clients",
    "aud": "https://api.example.com",
    "iat": time(),
    "exp": time() + 3600,
    "azp": "mK3brgMY0GIMox40xKWcUZBbv2Xs0YdG",
    "scope": "read:clients,read:actions",
    "gty": "client-credentials",
    "permissions": [],
}

NO_ACTIONS_READ_PERMISSION_TOKEN_PAYLOAD = {
    "iss": "https://my-domain.us.auth0.com/",
    "sub": "user@clients",
    "aud": "https://api.example.com",
    "iat": time(),
    "exp": time() + 3600,
    "azp": "mK3brgMY0GIMox40xKWcUZBbv2Xs0YdG",
    "scope": "read:clients",
    "gty": "client-credentials",
    "permissions": ["read:manager-features"],
}

MANAGER_TOKEN_PAYLOAD = {
    **VALID_TOKEN_PAYLOAD,
    "permissions": ["read:manager-features"],
}


class ApplicationsDetailsApiViewTest(SimpleTestCase):

    def test_get_applications_details_api_view_without_token_returns_unauthorized(self):
        response = self.client.get(reverse('applications-details'))

        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(), {'message': 'Authentication credentials were not provided.'}
        )

    def test_get_applications_details_api_view_with_invalid_token_returns_unauthorized(self):
        response = self.client.get(
            reverse('applications-details'), HTTP_AUTHORIZATION="Bearer invalid-token"
        )

        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(), {'message': "Given token not valid for any token type"}
        )

    @patch.object(TokenBackend, 'decode')
    def test_get_applications_details_api_view_without_manager_features_token_returns_forbidden(self, mock_decode):
        mock_decode.return_value = VALID_TOKEN_PAYLOAD

        response = self.client.get(
            reverse('applications-details'), HTTP_AUTHORIZATION="Bearer valid-token"
        )

        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(
            response.json(),
            {
                'error': "insufficient_permissions",
                'error_description': "You do not have permission to perform this action.",
                'message': "Permission denied"
            },
        )

    @patch.object(TokenBackend, 'decode')
    def test_get_applications_details_api_view_without_read_actions_token_returns_forbidden(self, mock_decode):
        mock_decode.return_value = NO_ACTIONS_READ_PERMISSION_TOKEN_PAYLOAD

        response = self.client.get(
            reverse('applications-details'), HTTP_AUTHORIZATION="Bearer valid-token"
        )

        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(
            response.json(),
            {
                'status_code': 403,
                'error_description': "insufficient_scope",
                'message': "Insufficient scope, expected any of: read:actions",
                'exception': True,
            },
        )
    
    @patch.object(TokenBackend, 'decode')
    def test_get_applications_details_api_view_with_manager_token_returns_ok(self, mock_decode):
        mock_decode.return_value = MANAGER_TOKEN_PAYLOAD
        
        response = self.client.get(
            reverse('applications-details'), HTTP_AUTHORIZATION="Bearer valid-token"
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'Default App': {'client_id': 'aWpgOkB2EMxPRXws5ucHekALCv0wc4fP', 'actions': []}, 'Auth0 Management API (Test Application)': {'client_id': 'lO7kZ6zsgZDYAkHBY9plH1MVXTP7yoA2', 'actions': [{'name': 'action_two', 'status': 'deployed', 'trigger_id': 'post-login'}]}, 'API Explorer Application': {'client_id': 'eBQasLhcDEToTHmlZIFybiYzP4NVOzhD', 'actions': [{'name': 'Test Action', 'status': 'deployed', 'trigger_id': 'credentials-exchange'}, {'name': 'action_two', 'status': 'deployed', 'trigger_id': 'post-login'}, {'name': 'action_four', 'status': 'built', 'trigger_id': 'credentials-exchange'}]}, 'Challenge App': {'client_id': 'ZrB9i5fmY3PSYzbXLb5z2UmzYZ7GNo5n', 'actions': [{'name': 'action_two', 'status': 'deployed', 'trigger_id': 'post-login'}]}, 'Challenge Client': {'client_id': 'P8OYtDmgdes7Mru6HKthiIhvsf5YBCl7', 'actions': [{'name': 'Test Action', 'status': 'deployed', 'trigger_id': 'credentials-exchange'}, {'name': 'action_two', 'status': 'deployed', 'trigger_id': 'post-login'}]}, 'Challenge Server (Test Application)': {'client_id': 'toRtC6e7RWKquV2sjqbX78zF2R17ni8f', 'actions': []}})
