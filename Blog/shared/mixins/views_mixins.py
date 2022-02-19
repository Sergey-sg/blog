from typing import Union

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from slugify import slugify

from apps.accounts.tokens import account_activation_token


class ScoreCommentMixin:
    @staticmethod
    def get_score_for_comment(author, article, model):
        """return list [True, Score] or [False]"""
        try:
            score = model.objects.get(author=author, article=article)
            if score:
                return [True, score]
        except Exception:
            return [False]
        else:
            return [False]


class CommentScoreMixin:
    @staticmethod
    def get_comments_for_score(author, article, model):
        """return list [True, CommentArticle] or [False]"""
        try:
            comments = model.objects.filter(author=author, article=article)
            if comments:
                return [True, comments]
        except Exception:
            return [False]
        else:
            return [False]


# class SendSubscriptionMixin:
#
#     @staticmethod
#     def send_to_subscriptions(article):
#         user = get_user_model()
#         to_emails = user.objects.filter(subscription__pk=article.author.pk) # .only('email')
#         domain = Site.objects.get_current().domain
#         messages = None
#         author_name = article.author.get_full_name() or article.author.email
#         for sub_user in to_emails:
#             subscript_user_name = sub_user.get_full_name() or sub_user.email
#             message = (
#                 _('Новая статья в вашей подписке'),
#                 f"""{subscript_user_name} {_('Вы подписаны на')} {author_name},
#                  {_('у автора появилась новая статья')} "{article.title}"
#                  {_('перейдите по адресу к статье')} {domain}{reverse_lazy('article_detail', kwargs={'slug':article.slug})}
#                  """,
#                 settings.EMAIL_HOST_USER,
#                 [sub_user.email],
#             )
#             if messages is None:
#                 messages = (message,)
#             else:
#                 messages += (message,)
#         if messages is not None:
#             send_mass_mail(messages)


class CurrentSlugMixin:

    def get_current_slug(self, slug, alt, model, pk) -> str:
        """return current unique slug for model"""
        if not slug:
            slug = slugify(alt)
        else:
            slug = slugify(slug)
        try:
            origin = model.objects.get(slug=slug)
        except Exception:
            origin = False
        if origin and origin.pk != pk:
            while True:
                numb = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                if slug[-1] in set(numb):
                    slug = slug[:-1] + str(int(slug[-1]) + 1)
                else:
                    slug += '1'
                try:
                    model.objects.get(slug=slug)
                except Exception:
                    break
        return slug


def send_activate_message(user, request) -> None:
    """send message for new user with activate linc"""
    to_email = user.email
    current_site = get_current_site(request)
    mail_subject = _('Activating your account')
    message = render_to_string(
        'registration/msg.jinja2',
        {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
    )
    send_mail(
        mail_subject,
        from_email=settings.EMAIL_HOST_USER,
        message=_('link to confirm email and complete registration'),
        recipient_list=[to_email],
        html_message=message,
    )
