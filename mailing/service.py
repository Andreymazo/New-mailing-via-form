# from django.conf import settings
from smtplib import SMTPResponseException, SMTPRecipientsRefused

from django.core.mail import send_mail

from config import settings
from mailing.models import Mailinglog


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
