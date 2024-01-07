from django.http import JsonResponse
from django.http.request import HttpRequest
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_csrf_token(request: HttpRequest) -> JsonResponse:
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})
