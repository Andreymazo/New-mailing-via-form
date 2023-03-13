from django.contrib.auth.views import LogoutView
from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import SigninView, SignupView, ClientListView, VerifySuccessView, PasswordResetConfirmView, \
    MssgCreateView, MssgUpdateView, EmailsListView, message, \
    ClientUpdateView, MssgListView, MssgUpdateViewWithSubjectPk, ClientUpdateViewWithSubject, \
    CustomPasswordResetConfirmView, CustomPasswordResetDoneView, CustomPasswordResetCompleteView, \
    verify_email, simple_reset_password, UserProfileView, CustomPasswordResetView  # , ClientCreateView,

# mailing,MssgUpdateViewWithSubjectPk,
app_name = MailingConfig.name

urlpatterns = [
    # path('', mailing, name='login'),

    path('', SigninView.as_view(template_name='mailing/login.html'), name='login'),#'template_name=mailing/Client1.html'
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', SignupView.as_view(), name='register'),
    path('register/success/', SignupView.as_view(template_name='mailing/signup_success.html'), name='register_success'),
    path('password/reset/', CustomPasswordResetView.as_view(template_name='mailing/password_reset_form.html'), name='password_reset'),
    path('password/reset/<uidb64>/confirm/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('register_success', VerifySuccessView.as_view(template_name='mailing/Client_list.html'), name='register_success'),
    path('verify/<str:token>/', verify_email, name='verify_email'),

    path('simple/reset/', simple_reset_password, name='simple_reset'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    path('client_logout', LogoutView.as_view(), name='logout'),
    # path('client_register', ClientListView.as_view(), name='register'),
    path('Client_list/', ClientListView.as_view(template_name='mailing/Client_list.html'), name='Client_list'),

    # path('Client_update', ClientUpdateView.as_view(template_name='mailing/Client_update.html'), name='Client_update'),
    path('Client_update/<int:pk>', ClientUpdateView.as_view(template_name='mailing/Client_update.html'), name='Client_update'),
    path('Client_update/<int:pk>/subjects/', ClientUpdateViewWithSubject.as_view(template_name='mailing/Client_withsubject.html'), name='Client_withsubject'),
    path('Mssg_list_list/', MssgListView.as_view(template_name='mailing/Mssg_list.html'), name='Mssg_list_list'),
    path('Mssg_list/', MssgCreateView.as_view(template_name='mailing/Mssg_list.html'), name='Mssg_list'),
    # path('Mssg_list/', message, name='Mssg_list'),
    path('Mssg_list/<int:pk>', MssgUpdateView.as_view(template_name='mailing/Mssg_list.html'), name='Mssg_list'),
    path('Mssg_list/<int:pk>/subject_pk/', MssgUpdateViewWithSubjectPk.as_view(template_name='mailing/Mssg_withsubjectPk.html'), name='Mssg_list_pk'),
    #
    path('Emails_list/', EmailsListView.as_view(template_name='mailing/Mssg_list.html'), name='Emails_list'),

# Client_list/<int:pk>
]
# urlpatterns = [path('', SigninView.as_view(template_name='spa/login.html'), name='login'),
#                path('register', SignupView.as_view(template_name='spa/register.html'), name='register'),
#                path('home/', SignupView.as_view(template_name='spa/home.html'), name='home')
