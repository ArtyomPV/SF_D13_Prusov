from .models import User, Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import timedelta


def sending_mail(today):
    """
    Рассылка новых объявлений раз в неделю всем пользователям
    """
    start_week = today - timedelta(days=7)
    end_week = today

    for user_instance in User.objects.all():
        email = user_instance.email
        username = user_instance.username
        post_list = Post.objects.filter(published_date=(start_week, end_week))

        html_content = render_to_string(
            'pokorum/reminder_week.html',
            context=
            {'subscriber_posts': post_list,
             'username': username,
             'domain_url': settings.DOMAIN,}
        )

        msg = EmailMultiAlternatives(
            subject="Новые объявления за неделю",
            from_email='artpv@yandex.ru',
            to=[email,]
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()