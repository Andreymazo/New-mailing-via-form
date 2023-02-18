from django.conf import settings
from django.core.mail import send_mail


def mailing():
    emails = ['andreymazo@mail.ru', 'andreymazo2@mail.ru']
    res = send_mail(
        subject=' test subject ',
        message=f' test message ',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=False,
        auth_user=None,
        auth_password=None,
        connection=None,
        html_message=None,
    )
    print(f'Pechataem res {res}')


mailing()

#############################################

# for i in emails:
# if request.method == 'GET':
#     res = "Zaglushka chtobi ne otpravlyat pisma"
#     # res = send_mail(
#     #     subject=' test subject ',
#     #     message=f' test message ',
#     #     from_email=settings.EMAIL_HOST_USER,
#     #     recipient_list=emails,
#     #     fail_silently=False,
#         # auth_user=None,
#         # auth_password=None,
#         # connection=None,
#         # html_message=None,
#     # )
#
#     # context = {'object_list': Mssg.objects.all()}
#     print(f'Messg sent >>>>>>, Result, {res}')#{Client.comment_set.count}
#     context = {'res':res}
#     return render(request, 'mailing/Client1.html', context)
