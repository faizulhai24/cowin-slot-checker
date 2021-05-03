import logging
import datetime
from celery import shared_task
from cowin.common.cache.redis import redis
from cowin.common.helpers.slot_checker import SlotChecker
from cowin.common.services.verloop_whatsapp_api import verloop_whatsapp_api
from cowin.common.helpers.message_generator import get_message_params
from .models import User

logger = logging.getLogger(__name__)

DISTRICT_IDS_SET_KEY = 'district_ids'
NUM_WEEKS = 5


@shared_task(name='core.tasks.add_user_to_district')
def add_user_to_district_cache(user_id, district_ids):
    for district_id in district_ids:
        key = 'district_id-{}'.format(district_id)
        redis.add_to_set(key, user_id)


@shared_task(name='core.tasks.add_district_ids_to_cache')
def add_district_ids_to_cache(district_ids):
    return redis.add_to_set(DISTRICT_IDS_SET_KEY, *district_ids)


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
        district_id = district_id.decode('utf-8')
        free_slots = []
        for date in dates:
            sc = SlotChecker()
            slots = sc.check(district_id, date)
            free_slots.extend(slots)

        if free_slots:
            send_message_for_district.delay(district_id, free_slots)
    return


@shared_task(name='core.tasks.send_otp')
def send_otp(phone_number, name, otp):
    return verloop_whatsapp_api.send_otp(phone_number, {
        'name': name,
        'number': otp
    })


@shared_task(name='core.tasks.send_message_for_district')
def send_message_for_district(district_id, free_slots):
    key = 'district_id-{}'.format(district_id)
    user_ids = list(redis.get_members_from_set(key))
    params = get_message_params(free_slots)

    if params is None:
        return
    for user_id in user_ids:
        user_id = user_id.decode('utf-8')
        send_message_for_user(user_id, params)


@shared_task(name='core.tasks.send_message_for_user')
def send_message_for_user(user_id, params):
    user = User.objects.get(pk=user_id)
    if user.verified and user.message_consent:
        params['name'] = user.first_name
        logger.info("Sending availability message")
        verloop_whatsapp_api.send_slot_availability(user.phone_number, params)
