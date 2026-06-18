import json
import logging

import httpx

_http_logger = logging.getLogger("http_trace")


def _pretty(raw: bytes) -> str:
    try:
        return json.dumps(json.loads(raw), indent=2)
    except (json.JSONDecodeError, ValueError):
        return raw.decode("utf-8", "replace")


async def _log_exchange(response: httpx.Response) -> None:
    request = response.request
    _http_logger.info("--> %s %s", request.method, request.url)
    if request.content:
        _http_logger.info("--> request body:\n%s", _pretty(request.content))
    await response.aread()  # body is not read yet inside the hook
    _http_logger.info("<-- status %s", response.status_code)
    _http_logger.info("<-- response body:\n%s", _pretty(response.content))
