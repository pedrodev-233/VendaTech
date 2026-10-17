import logging

logger = logging.getLogger(__name__)


class UserIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        ip = request.META.get("REMOTE_ADDR", "Desconhecido")

        print(
            f"[{response.status_code}] "
            f"IP: {ip} | "
            f"{request.method} | "
            f"{request.path}",
            flush=True,
        )

        return response