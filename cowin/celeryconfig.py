from datetime import timedelta

from django.conf import settings

broker_url = settings.BROKER_URL

beat_schedule = {
    'poll_slots': {
        'task': 'core.tasks.check_slots',
        'schedule': timedelta(minutes=3),
    },
}

result_backend = 'redis://localhost:6379'

timezone = 'UTC'

worker_disable_rate_limits = True

worker_max_tasks_per_child = 50

worker_hijack_root_logger = False

task_track_started = True

task_always_eager = False

task_ignore_result = True

task_send_sent_event = True

task_soft_time_limit = 1800  # 30mins
