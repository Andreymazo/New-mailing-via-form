# from django.conf import settings
# from django.core.mail import send_mail
#
# from mailing.models import Mailinglog
#
#
# def send_mail(user_email):
#     res = send_mail(
#                         subject=' test subject ',
#                         message=f' test message ',
#                         from_email=settings.EMAIL_HOST_USER,
#                         recipient_list=i,
#                         fail_silently=False,
#                         auth_user=None,
#                         auth_password=None,
#                         connection=None,
#                         html_message=None,
#                     )
#     if res:
#         Mailinglog.objects.create(
#             ####Zapisivaem pochtu, resultat otpravki i vremia samo zapisivaetsia#########
#             mailing=i,
#             result=res
#         )
