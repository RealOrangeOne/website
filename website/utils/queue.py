from typing import Callable

from django.conf import settings
from django_rq import get_queue


def enqueue_or_sync(
    job_func: Callable, args: list | None = None, kwargs: dict | None = None
) -> None:
    """
    Run a task now, or put in RQ
    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    if settings.USE_REDIS_QUEUE:
        get_queue().enqueue(job_func, args=args, kwargs=kwargs)
    else:
        job_func(*args, **kwargs)
