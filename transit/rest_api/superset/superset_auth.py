import json
import requests

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET

from rest_framework import (
    permissions,
    status
)
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.response import Response
from rest_framework_simplejwt import authentication

from transit.settings import (
    SUPERSET_ADMIN,
    SUPERSET_PASSWORD,
    SUPERSET_HOST,
    SUPERSET_FIRSTNAME_DASHBOARD,
    SUPERSET_LASTNAME_DASHBOARD,
    SUPERSET_USERNAME_DASHBOARD
)


@require_GET
@api_view(('GET',))
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def superset_guest_token(request):
    embedded_id = request.query_params.get('embedded_id', None)
    if embedded_id is None:
        raise ValidationError(_('Bad request. Embedded ID is required!'))

    auth_token_response = _get_superset_auth_token()
    if auth_token_response.status_code != status.HTTP_200_OK:
        raise ValidationError(auth_token_response.json())

    guest_token_response = _get_superset_guest_token(auth_token_response, embedded_id)
    if guest_token_response.status_code != status.HTTP_200_OK:
        raise ValidationError(guest_token_response.json())

    guest_token_response = guest_token_response.json()
    return Response(guest_token_response["token"])


def _get_superset_auth_token():
    auth_access_token = _build_superset_access_token_payload()
    return requests.post(
        F"{SUPERSET_HOST}/api/v1/security/login",
        data=json.dumps(auth_access_token),
        headers={
            'Content-type': 'application/json',
        }
    )


def _get_superset_guest_token(auth_token_response, embedded_id):
    auth_token_response = auth_token_response.json()
    guest_token_payload = _build_superset_guest_token_payload(embedded_id)
    return requests.post(
        F"{SUPERSET_HOST}/api/v1/security/guest_token/",
        data=json.dumps(guest_token_payload),
        headers={
            'Content-type': 'application/json',
            "Authorization": f"Bearer {auth_token_response['access_token']}"
        }
    )


def _build_superset_access_token_payload():
    return {
        "password": SUPERSET_PASSWORD,
        "provider": "db",
        "refresh": True,
        "username": SUPERSET_ADMIN,
    }


def _build_superset_guest_token_payload(embedded_id):
    return {
        "user": {
            "username": SUPERSET_USERNAME_DASHBOARD,
            "first_name": SUPERSET_FIRSTNAME_DASHBOARD,
            "last_nane": SUPERSET_LASTNAME_DASHBOARD
        },
        "resources": [{
            "type": "dashboard",
            "id": embedded_id
        }],
        "rls": []
    }
