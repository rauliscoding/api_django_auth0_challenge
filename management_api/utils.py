from auth0.v3.authentication import GetToken
from django.conf import settings


def get_management_api_token():
    """
    Obtain a management API token
    """
    domain = settings.AUTH0_DOMAIN
    non_interactive_client_id = settings.AUTH0_CLIENT_ID
    non_interactive_client_secret = settings.AUTH0_CLIENT_SECRET

    get_token = GetToken(domain)
    token = get_token.client_credentials(non_interactive_client_id,
        non_interactive_client_secret, 'https://{}/api/v2/'.format(domain))
    mgmt_api_token = token['access_token']

    return mgmt_api_token
