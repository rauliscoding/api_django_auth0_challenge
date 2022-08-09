from xml.dom import WrongDocumentErr
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from auth0.v3.management import Auth0
from django.http import JsonResponse
from authz.permissions import HasManagerPermission
from .utils import get_management_api_token
from .constants import (CLIENT_NAME, CLIENT_ID, CLIENT_ACTIONS, ACTION_NAME, ID, 
                        ACTION_STATUS, ACTION_CODE, TRIGGER_ID, SUPPORTED_TRIGGERS,
                        ALL_CHANGES_DEPLOYED, STATUS_BUILT, STATUS_DEPLOYED)


class ApplicationsDetails(APIView):
    """
    View to retrieve the applications, the Actions that apply to each 
    application and the type of trigger each Action is bound to.
    """
    
    permission_classes = [IsAuthenticated, HasManagerPermission]

    def get(self, request, format=None):
        """
        Return a JSON with the applications details
        """

        # Instantiate return dict
        applications_details_dict = dict()

        # Instantiate an Auth0 object with a domain and a Management API v2 token
        auth0 = Auth0(settings.AUTH0_DOMAIN, get_management_api_token())
        
        # Get all available clients
        clients_list = auth0.clients.all()
        if clients_list:
            for client in clients_list:
                applications_details_dict[client.get(CLIENT_NAME)] = {
                    CLIENT_ID:      client[CLIENT_ID],
                    CLIENT_ACTIONS: [],
                }

            # Remove 'All Applications' entry
            del applications_details_dict['All Applications']

            # Get all available actions
            actions_list = auth0.actions.get_actions()[CLIENT_ACTIONS]

            # Get the clients names
            clients_names_list = applications_details_dict.keys()

            # Iterate through clients
            for client_name in clients_names_list:

                #Iterate through actions
                for action in actions_list:

                    # Check if the client is referenced in the action's 'code' value and add it to the actions list
                    if client_name in action[ACTION_CODE]:
                        applications_details_dict[client_name][CLIENT_ACTIONS].append({
                            ACTION_NAME: action[ACTION_NAME],
                            ACTION_STATUS: STATUS_DEPLOYED if action[ALL_CHANGES_DEPLOYED] else STATUS_BUILT,
                            TRIGGER_ID: action[SUPPORTED_TRIGGERS][0][ID]
                        })
        
        return JsonResponse(applications_details_dict, safe=False, status=status.HTTP_200_OK)