from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mass_mail
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


# @shared_task
# def print_text(text):
#     print(text)
#     return f'The text "{text}" printed'


@shared_task(bind=True, default_retry_delay=5*60)
def send_to_subscriptions(self, author_pk, title, slug):
    """send mass mail for subscriptions"""
    try:
        user = get_user_model()
        author = user.objects.get(pk=author_pk)
        to_emails = user.objects.filter(subscription__pk=author.pk)
        domain = Site.objects.get_current().domain
        messages = None
        author_name = author.get_full_name() or author.email
        for sub_user in to_emails:
            subscript_user_name = sub_user.get_full_name() or sub_user.email
            message = (
                _('Новая статья в вашей подписке'),
                f"""{subscript_user_name} {_('Вы подписаны на')} {author_name},
                 {_('у автора появилась новая статья')} "{title}"
                 {_('перейдите по адресу к статье')} {domain}{reverse_lazy('article_detail', kwargs={'slug':slug})}
                 """,
                settings.EMAIL_HOST_USER,
                [sub_user.email],
            )
            if messages is None:
                messages = (message,)
            else:
                messages += (message,)
        if messages is not None:
            send_mass_mail(messages)
            print('Mass mail send')
        return f'Mass mail send for article {title}'
    except Exception as exc:
        # retry(countdown=60) задает перезапуск задачи через 60 сек
        raise self.retry(exc=exc, countdown=60)
