import base64
import json
from flask import request


def _api_gateway_before_request():
    userinfo = request.headers.get('X-Apigateway-Api-Userinfo')

    if not userinfo:
        request.user_token = None
        return

    userinfo = userinfo + '=' * (4 - len(userinfo) % 4)

    try:
        userinfo_decoded = base64.urlsafe_b64decode(userinfo)
        request.user_token = json.loads(userinfo_decoded)
    except Exception:
        request.user_token = None
        return


def setup_apigateway(app):
    app.before_request(_api_gateway_before_request)
