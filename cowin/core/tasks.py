import logging
import datetime
from celery import shared_task
from cowin.common.cache.redis import redis
from cowin.common.helpers.slot_checker import SlotChecker

logger = logging.getLogger(__name__)

DISTRICT_IDS_SET_KEY = 'district_ids'
NUM_WEEKS = 5


@shared_task(name='core.tasks.check_slots')
def check_slots(*args, **kwargs):
    district_ids = list(redis.get_members_from_set(DISTRICT_IDS_SET_KEY))
    if not district_ids:
        return
    now = datetime.datetime.now()
    dates = []
    for i in range(NUM_WEEKS):
        target_time = now + datetime.timedelta(days=7 * i)
        dates.append(target_time.strftime("%d-%m-%Y"))

    for district_id in district_ids:
        free_slots = []
        for date in dates:
            sc = SlotChecker()
            slots = sc.check(district_id, date)
            free_slots.extend(slots)

        if free_slots:
            send_message_for_district(district_id, free_slots).delay()
    return


@shared_task(name='core.tasks.add_user_to_district')
def add_user_to_district_cache(user_id, district_ids):
    for district_id in district_ids:
        key = 'district_id-{}'.format(district_id)
        redis.add_to_set(key, user_id)


@shared_task(name='core.tasks.add_district_ids_to_cache')
def add_district_ids_to_cache(district_ids):
    return redis.add_to_set(DISTRICT_IDS_SET_KEY, *district_ids)


@shared_task(name='core.tasks.send_message_for_district')
def send_message_for_district(district_id, free_slots):
    key = 'district_id-{}'.format(district_id)
    user_ids = list(redis.get_members_from_set(key))
    # {
    #     'center_name': center['name'],
    #     'district_name': center['district_name'],
    #     'date': session['date'],
    #     'fee_type': center['fee_type'],
    #     'vaccine': session['vaccine'],
    #     'available_capacity': session['available_capacity']
    # }


