import logging
from time import perf_counter

logger = logging.getLogger(__name__)


class RequestTimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = perf_counter()
        response = self.get_response(request)
        response_time = perf_counter() - start_time
        logger.info(f'Запрос на {request.path} отработал за {response_time} сек.')
        response['Ellapsed-Time'] = str(response_time)
        return response
