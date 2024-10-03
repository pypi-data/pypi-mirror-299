import base64
import json
from flask import Flask, request, g


def _api_gateway_before_request() -> None:
    userinfo = request.headers.get('X-Apigateway-Api-Userinfo')

    if not userinfo:
        g.user_token = None
        return

    userinfo = userinfo + '=' * (4 - len(userinfo) % 4)

    try:
        userinfo_decoded = base64.urlsafe_b64decode(userinfo)
        g.user_token = json.loads(userinfo_decoded)
    except Exception:
        g.user_token = None
        return


def setup_apigateway(app: Flask) -> None:
    app.before_request(_api_gateway_before_request)
