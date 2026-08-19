from celery import Celery
from app.core.config import get_settings
app=Celery("originlens",broker=get_settings().redis_url,backend=get_settings().redis_url)
app.conf.update(worker_prefetch_multiplier=1,task_acks_late=True)
