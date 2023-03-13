# from django.conf import settings
from smtplib import SMTPResponseException, SMTPRecipientsRefused

from django.core.mail import send_mail
from django.template import context

from config import settings
from mailing.models import Mailinglog, Client

from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from mailing.models import Client


def set_verify_token_and_send_mail(new_user):
    """
        Деактивировать пользователя, установить токен и сроки жизни
        TODO: отправить письмо на почту со ссылкой
    """
    now = datetime.now(pytz.timezone(settings.TIME_ZONE))
    new_user.is_active = False
    print(new_user)
    new_user.verify_token = Client.objects.make_random_password(length=20)
    new_user.verify_token_expired = now + timedelta(hours=72)
    new_user.save()

    link_to_verify = reverse('mailing:verify_email', args=[new_user.verify_token])
    # TODO: сделать красивое письмо
    # http://localhost:8088/users/verify/woefhowuhefoqihwefiqf/
    # render_to_string('mailing/Client_detail.html', context)##Sdelat pismo krasivo
    send_mail(
        subject='Подтвердите почту для BUBE-7',
        message=f'{settings.BASE_URL}{link_to_verify}',#BASE_URL=os.getenv('BASE_URL')
        recipient_list=[new_user.email],
        from_email=settings.EMAIL_HOST_USER
    )
    # return new_user.verify_token


def generate_password_and_end_mail(user):
    new_password = Client.objects.make_random_password(length=12)
    user.new_password = make_password(new_password)
    user.save()
    send_mail(
        subject='Новый пароль',
        message=f'{new_password}',
        recipient_list=[user.email],
        from_email=settings.EMAIL_HOST_USER
    )
def send(user_email):

    try:
        res = send_mail(
                                    subject=' test subject ',
                                    message=f' test message ',
                                    from_email=settings.EMAIL_HOST_USER,
                                    recipient_list=[user_email],
                                    fail_silently=False,
                                    auth_user=None,
                                    auth_password=None,
                                    connection=None,
                                    html_message=None,

        )
        if res:
            Mailinglog.objects.create(
                ####Zapisivaem pochtu, resultat otpravki i vremia samo zapisivaetsia#########
                mailing=user_email,
                result=res
            )
    except SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        if error_code == 550:  # возможно, по-другому надо доставать, типа e.errno
            print("Error code:" + f'{error_code}')
            print("Message:" + f'{error_message}')
        pass
    except SMTPRecipientsRefused as e:
        print(e)
        pass

# from mailing.models import Mailinglog
#
#
# def send_mail(user_email):
#     res = send_mail(
#                         subject=' test subject ',
# #                         message=f' test message ',
# #                         from_email=settings.EMAIL_HOST_USER,
# #                         recipient_list=i,
# #                         fail_silently=False,
# #                         auth_user=None,
# #                         auth_password=None,
# #                         connection=None,
# #                         html_message=None,
#                     )
#     if res:
# #         Mailinglog.objects.create(
# #             ####Zapisivaem pochtu, resultat otpravki i vremia samo zapisivaetsia#########
# #             mailing=i,
# #             result=res
# #         )
