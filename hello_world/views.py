from django.http import JsonResponse
from rest_framework.views import exception_handler
from auth0.v3.exceptions import Auth0Error
from rest_framework.response import Response

def not_found(request, *args, **kwargs):
    return JsonResponse(data={"message": "Not Found"}, status=404)


def app_error(request, *args, **kwargs):
    return JsonResponse(data={"message": "Server Error"}, status=500)

def api_exception_handler(exc, context=None):
    if isinstance(exc, Auth0Error):
        return Response({
            'status_code': exc.status_code,
            'error_description': exc.error_code,
            'message': exc.message,
            'exception': True,
            },
            status=exc.status_code
        )
    else:
        response = exception_handler(exc, context=context)

        if response.status_code == 403:
            response.data = {
                'error': 'insufficient_permissions',
                'error_description': response.data.get('detail', 'API Error'),
                'message': 'Permission denied'
            }
        elif response and isinstance(response.data, dict):
            response.data = {'message': response.data.get('detail', 'API Error')}
        else:
            response.data = {'message': 'API Error'}
        return response