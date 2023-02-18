from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from mailing.models import Mssg, Client, Emails, Mailinglog, Subject
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

# def gg(self, *args, **options):
#     jj = [{"g": 2}]
#     for i in jj:
#         rec = i[0]
#         rec.save()
class Command(BaseCommand):

    # def handle(self, *args, **options):
    #     emails = ['andreymazo@mail.ru', 'andreymazo2@mail.ru']
    #     res = send_mail(
    #         subject=' test subject ',
    #         message=f' test message ',
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=emails,
    #         fail_silently=False,
    #         auth_user=None,
    #         auth_password=None,
    #         connection=None,
    #         html_message=None,
    #     )
    #     print(res)

    # for i in m.:
    #     # print(i.email, i.name)
    #     print(i.text, i.topic, i.status)
    def handle(self, *args, **options):

        # H = set()# Mozhno iskluchit povtorenia otpravki odnih i teh zhe soobshenii
        def mailing():
            h = Emails.objects.all()
            m = Mssg.objects.all()
            mm = Client.objects.all()
            f = Subject.objects.all()

            # for i in h:##Emails
            #     for ii in mm:##Imena
            #     # print(ii)
            for iii in m:  ##Soobshenia
            #     print(iii.text)###Vidast temu soobshenia
            #             print(iii)
                for iiii in f:
            #     # print(iiii.email)#Cherez subject spisok emailov dlia otpravki
            #     print(iiii.text)

                # emails = ['andreymazo@mail.ru', 'andreymazo2@mail.ru']
                        res = send_mail(
                            subject=f'{iii.text}',
                            message=f'{iiii.text}',
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[iiii.email],
                            fail_silently=False,
                            auth_user=None,
                            auth_password=None,
                            connection=None,
                            html_message=None,
                        )
                        print(f'Pechataem res {res}')
                        if res:
                            Mailinglog.objects.create(
                                        ####Zapisivaem pochtu, resultat otpravki i vremia samo zapisivaetsia#########
                                    mailing=iiii.email,
                                    result=res
                                                    )
            mailing()
            # def mailing(request):#
        # m = Mssg.objects.all()

        # m = Mssg.objects.get(pk=1)
        # print(m)
        # mm = Client.objects.all()
        # for i in mm:
        #     print(i.name)

        # m = Emails.objects.filter(email__contains="@")###Delaem view i prohodim po ney kak vizivaem funcciu i filtruem po Clientu
        # subj = Mssg.objects.all()
        # for i in m:
        #     # print(i)
        #
        #     try:
        #         for ii in subj:
        #             # print(i.text)
        #             res = send_mail(
        #                                 subject=f'{ii.topic}',
        #                                 message=f' {ii.text}',
        #                                 from_email=settings.EMAIL_HOST_USER,
        #                                 recipient_list=[i],
        #                                 fail_silently=False,
        #                                 auth_user=None,
        #                                 auth_password=None,
        #                                 connection=None,
        #                                 html_message=None,
        #                             )
        #             if res:
        #                 Mailinglog.objects.create(
        #                     ####Zapisivaem pochtu, resultat otpravki i vremia samo zapisivaetsia#########
        #                     mailing=i,
        #                     result=res
        #                                 )
        #     except BadHeaderError:
        #         return HttpResponse('Invalid header found.')
        # return HttpResponseRedirect('/contact/thanks/')
    # else:
    #     # In reality we'd use a form class
    #     # to get proper validation errors.
    #     return HttpResponse('Make sure all fields are entered and valid.')
# def send_email(request):
#     subject = request.POST.get('subject', '')
#     message = request.POST.get('message', '')
#     from_email = request.POST.get('from_email', '')
#     if subject and message and from_email:
#         try:
#             send_mail(subject, message, from_email, ['admin@example.com'])
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')
#         return HttpResponseRedirect('/contact/thanks/')
#     else:
#         # In reality we'd use a form class
#         # to get proper validation errors.
#         return HttpResponse('Make sure all fields are entered and valid.')