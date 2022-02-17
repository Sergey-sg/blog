from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')

app = Celery('Blog')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# app.conf.beat_schedule = {
#     'print-text-every-1-min': {
#                 # Регистрируем задачу. Для этого в качестве значения ключа task
#                 # Указываем полный путь до созданного нами ранее таска(функции)
#                 'task': 'apps.blog.tasks.print_text',
#
#                  # Периодичность с которой мы будем запускать нашу задачу
#                  # minute='*/1' - говорит о том, что задача должна выполнятся каждые 5 мин.
#                 'schedule': crontab(minute='*/1'),
#
#                 # Аргументы которые будет принимать функция
#                 'args': (f'Это ==текст==, а это время - {datetime.now()}',),
#     }
# }
