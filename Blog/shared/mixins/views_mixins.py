from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mass_mail
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from apps.interaction.models import Score, CommentArticle


class ScoreCommentMixin:
    @staticmethod
    def get_score_for_comment(author, article):
        try:
            score = Score.objects.get(author=author, article=article)
            if score:
                return [True, score]
        except Exception:
            return [False]
        else:
            return [False]


class CommentScoreMixin:
    @staticmethod
    def get_comments_for_score(author, article):
        try:
            comments = CommentArticle.objects.filter(author=author, article=article)
            if comments:
                return [True, comments]
        except Exception:
            return [False]
        else:
            return [False]


class SendSubscriptionMixin:

    @staticmethod
    def send_to_subscriptions(article):
        user = get_user_model()
        to_emails = user.objects.filter(subscription__pk=article.author.pk) # .only('email')
        domain = Site.objects.get_current().domain
        messages = None
        author_name = article.author.get_full_name() or article.author.email
        for sub_user in to_emails:
            subscript_user_name = sub_user.get_full_name() or sub_user.email
            message = (
                _('Новая статья в вашей подписке'),
                f"""{subscript_user_name} {_('Вы подписаны на')} {author_name},
                 {_('у автора появилась новая статья')} "{article.title}"
                 {_('перейдите по адресу к статье')} {domain}{reverse_lazy('article_detail', kwargs={'slug':article.slug})}
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
