import os
import dotenv
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delicious_project.settings')

app = Celery('delicious_project')
app.config_from_object('django.conf:settings')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
dotenv.read_dotenv(env_file)
