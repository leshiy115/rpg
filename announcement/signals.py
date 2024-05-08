from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Announcement, Comment
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Comment)
def comment_to_anons(instance, created, **kwargs):
    if created and instance.author != instance.anons.author:


        html_content = render_to_string(
            'notification_created.html',
            {
                'user': instance.anons.author.username,
                'writer': instance.author.username,
                'anons': instance.anons.pk,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'{instance.anons.author.username.capitalize()}',
            from_email='lutsckov.o@yandex.ru',
            to=[instance.anons.author.email],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        # msg.send(fail_silently=True)


@receiver(pre_save, sender=Comment)
def request_accepted(instance, **kwargs):
    print(kwargs)


