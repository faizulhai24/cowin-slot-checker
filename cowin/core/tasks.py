import logging
from celery import shared_task
from cowin.common.cache.redis import redis

logger = logging.getLogger(__name__)

DISTRICT_IDS = ""

@shared_task(name='core.tasks.check_slots')
def check_slots(*args, **kwargs):
    pass


@shared_task(name='core.tasks.add_district_ids')
def add_district_ids(*args, **kwargs):
    pass

@shared_task(name='core.tasks.collect_district_ids')
def collect_district_ids(*args, **kwargs):
    pass