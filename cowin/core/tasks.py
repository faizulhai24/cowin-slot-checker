import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name='core.tasks.check_slots')
def check_slots(*args, **kwargs):
    print("Running through task")
    print("check_slots")