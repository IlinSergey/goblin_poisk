import datetime
import logging
from time import perf_counter
from typing import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class RequestTimerMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = perf_counter()
        response = self.get_response(request)
        response_time = perf_counter() - start_time
        logger.info(f'Запрос на {request.path} отработал за {response_time} сек.')
        response['Ellapsed-Time'] = str(response_time)
        return response


class VerboseLoggingMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        self._log_request(request)
        response = self.get_response(request)
        return response

    def _log_request(self, request: HttpRequest) -> None:
        logger.info(
            'Пришел запрос на %s в: %s с IP: %s',
            request.path,
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            self._get_client_ip(request),
            )

    def _get_client_ip(self, request: HttpRequest) -> str:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
