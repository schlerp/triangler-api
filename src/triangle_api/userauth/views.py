import json
import logging
from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from pydantic import BaseModel

LOGGER = logging.getLogger(__file__)

LOGIN_ERROR_MESSAGE = "Incorrect username or password!"
LOGOUT_ERROR_MESSAGE = "Logout was unsuccessful!"


class User(BaseModel):
    id: int
    username: str


class AuthResponse(BaseModel):
    success: bool
    user: Optional[User] = None
    error: Optional[str] = None


class LoginResponse(AuthResponse):
    ...


class LogoutResponse(AuthResponse):
    ...


@ensure_csrf_cookie
def csrf(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"csrfToken": get_token(request)})


@ensure_csrf_cookie
def login_user(request: HttpRequest) -> HttpResponse:
    """Authenticates a user and sets the appropriate headers/cookies for session"""
    username: Optional[str] = None
    password: Optional[str] = None
    try:
        login_request = json.loads(request.body.decode("utf-8"))

        username = login_request.get("username", None)
        password = login_request.get("password", None)
    except Exception as e:
        LOGGER.error("Login request was malformed!", exc_info=e)

    user: Optional[AbstractBaseUser] = None
    if username is None or password is None:
        login_response = LoginResponse(success=False, error=LOGIN_ERROR_MESSAGE)
        status_code = 422
    else:
        user = authenticate(request, username=username, password=password)

    login_response: LoginResponse
    status_code: int
    if user is not None:
        login(request, user)
        login_response = LoginResponse(
            success=True, user=User(id=user.pk, username=user.get_username())
        )
        status_code = 200
    else:
        login_response = LoginResponse(success=False, error=LOGIN_ERROR_MESSAGE)
        status_code = 401

    return JsonResponse(
        login_response.dict(),
        status=status_code,
    )


@csrf_exempt
def logout_user(request: HttpRequest) -> HttpResponse:
    """Logs a user out and clears the headers/cookies for session"""
    logout_response: LogoutResponse
    status_code: int
    try:
        logout(request)
        logout_response = LogoutResponse(success=True)
        status_code = 200
    except Exception as e:
        LOGGER.error("There was an error logging out user!", exc_info=e)
        logout_response = LogoutResponse(success=False, error=LOGOUT_ERROR_MESSAGE)
        status_code = 500
    return JsonResponse(logout_response.dict(), status=status_code)
