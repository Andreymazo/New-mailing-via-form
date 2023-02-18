import time
from django import  forms
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, CreateView, ListView, UpdateView, TemplateView

from mailing.forms import ClientForm, SignupForm, SigninForm, MssgForm, EmailsForm
from mailing.models import Client, Mssg, Emails, Subject


class Command(BaseCommand):

    def handle(self, *args, **options):
# def mailing(request):#
        m=Client.objects.select_related("topic", "comment").all()
        print(m)
#         emails1 = ['andreymazo@mail.ru', 'andreymazo2@mail.ru']
#         emails2 = ['andreymazo@mail.ru', 'andreymazo2@mail.ru']
#         emails=[emails1, emails2]
#         while Mssg.status:
#             for i in emails:
#                 time.sleep(m.Mssg.period)
#                 if request.method == 'GET':
#                 # res = "Zaglushka chtobi ne otpravlyat pisma"
#                 res = send_mail(
#                     subject=' test subject ',
#                     message=f' test message ',
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=i,
#                     fail_silently=False,
#                     auth_user=None,
#                     auth_password=None,
#                     connection=None,
#                     html_message=None,
#                 )
#                   if res:
#                       Attempt.objects.create(
#                           status = res,
#                           response=''
#                       )
#                 Mailinglog.objects.create(
#                     message=item.message,
#                     mailing=item,
#                     result=res
#                 )
# #
#                 # context = {'object_list': Mssg.objects.all()}
#                 print(f'Messg sent >>>>>>, Result, {res}')#{Client.comment_set.count}
#                 context = {'res':res}
#                 return render(request, 'mailing/Client1.html', context)
#
# from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
# Here’s an example view that takes a subject, message and from_email from the request’s POST data, sends that to admin@example.com and redirects to “/contact/thanks/” when it’s done
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

def message(request):
    context = {
        'object': Mssg.objects.all()
    }

    return render(request, 'mailing/Mssg_list.html', context)

class SigninView(LoginView):
    template_name = 'mailing/login.html'
    form_class = SigninForm


class SignupView(CreateView):
    template_name = 'mailing/register.html'
    model = Client
    form_class = SignupForm
    success_url = reverse_lazy('mailing:Client_list')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         self.object = form.save()
    #         set_verify_token_and_send_mail(self.object)
    #     return super().form_valid(form)
class VerifySuccessView(TemplateView):
    success_url = reverse_lazy('mailing:Client_list')
    template_name = 'mailing/register.html'

class ClientListView(ListView):
    model = Client
    form_class = ClientForm
    # success_url = reverse_lazy('mailing:Client_update')
    template_name = 'mailing/Client_list.html'
    # def get_queryset(self):#Pochemu to ne filtruet po useru, a vse ubiraet, poka zakommentim
    #     print(self.request.user)##email polzovatelia
    #     return Client.objects.filter(email=self.request.user)##filtruem po polzovatelu

class ClientView(CreateView):#Posle registracii/logina Client popadaet v etu formu, a ne na Client_list (emu znat vseh clientov ne nado
    #################Potom ClientListView zakommentiruu
    model = Client
    form_class = ClientForm
    success_url = 'mailing:Client_withsubject'##Posle sozdania perenapravliaem na obshuu stranicu
    template_name = 'mailing/Client_update.html'##Ishem modul bootstrap

    def form_valid(self, form):##Chtobi chuzhoe ne trogali
        if form.is_valid():
            form.save(commit=False)
            self.object.email = self.request.user##Dobaliaem pole - znachenie polzovatelia/ mozhet ne email, a name
            self.object.save()
        return super(ClientView, self).form_valid()

class ClientUpdateView(UpdateView):#Posle registracii/logina Client popadaet v etu formu, a ne na Client_list (emu znat vseh clientov ne nado
    #################Potom ClientListView zakommentiruu
    # success_url = 'Client_update'
    model = Client
    fields = '__all__'
    success_url = 'mailing:Client_withsubject'
class ClientUpdateViewWithSubject(CreateView):
    model = Mssg
    form_class = MssgForm
    success_url = reverse_lazy('mailing:Client_list')
    template_name = 'catalog/Client_withsubject.html'
#
#     # def clean_product_content(self):
#     #     t = ['казинo', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
#     #     if self.request.method == 'POST':
#     #         # form = ProductForm(request.POST, request.FILES)
#     #         for i in t:
#     #             if self.product_content == i:
#     #                 raise ValueError('Nedopustimie slova')
#     # def get_success_url(self):
#     #     return reverse('catalog:Product_list', args=[self.object.pk])
#
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        FormSet = inlineformset_factory(self.model, Subject, form=SubjectForm, extra=1)

        if self.request.method == 'POST':
            formset = FormSet(self.request.POST, instance=self.object)
        else:
            formset = FormSet(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        print(self.request.method)
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
                # send(form.instance.email)
            else:
                return super(ClientUpdateViewWithSubject, self).form_invalid(form)
        return super(ClientUpdateViewWithSubject, self).form_valid(form)
# class ProductCreateFormMore():
#     def context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         FormSet = inlineformset_factory(self.model, Product, form=ProductForm, extra=1)
#         if self.request.method == 'POST':
#             formset = FormSet(self.request.POST, instance=self.object)
#         else:
#             formset = FormSet(instance=self.object)
#         context_data['formset']=formset
#         return context_data

class ClientDetailView(UserPassesTestMixin, DetailView):##
    model = Client
    fields = '__all__'
    success_url = 'mailing:home'
    # def test_func(self):##Proverka est li prava u polzovatelia, chtobi ne lasil
    #     i = self.get_object()
    #     return i.email == self.request.user or self.request.user.has_perm

    # def get_context_data(self, request, pk, *args, **kwargs):
    #     context = super(ClientDetailView, self).get_context_data(**kwargs)
    #     context['something'] = Client.objects.filter(pk=self.kwargs.get('pk'))
    #     return context
class MssgListView(ListView):
    model = Mssg
    form_class = MssgForm
    # success_url = reverse_lazy('mailing:Emails_list')
    template_name = 'mailing/Mssg_list.html'
    # def get_context_data(self, request, pk, *args, **kwargs):
    #     context = super(MssgListView, self).get_context_data(**kwargs)
    #     context['something'] = Mssg.objects.filter(pk=self.kwargs.get('pk'))
    #     return context

class MssgCreateView(CreateView):
    model = Mssg
    form_class = MssgForm
    # fields = '__all__'
    success_url = reverse_lazy('mailing:Emails_list')
    template_name = 'mailing/Mssg_list.html'




class MssgUpdateView(UpdateView):
    model = Mssg
    form_class = MssgForm
    # fields = '__all__'
    success_url = reverse_lazy('mailing:Mssg_list_pk')
    template_name = 'mailing/Mssg_list.html'

class MssgUpdateViewWithSubjectPk(CreateView):
    model = Mssg
    form_class = MssgForm
    success_url = reverse_lazy('mailin:home')
    template_name = 'catalog/Mssg_withsubjectPk.html'
#
#     # def clean_product_content(self):
#     #     t = ['казинo', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
#     #     if self.request.method == 'POST':
#     #         # form = ProductForm(request.POST, request.FILES)
#     #         for i in t:
#     #             if self.product_content == i:
#     #                 raise ValueError('Nedopustimie slova')
#     # def get_success_url(self):
#     #     return reverse('catalog:Product_list', args=[self.object.pk])
#
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        FormSet = inlineformset_factory(self.model, Subject, form=SubjectForm, extra=1)

        if self.request.method == 'POST':
            formset = FormSet(self.request.POST, instance=self.object)
        else:
            formset = FormSet(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        print(self.request.method)
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
                # send(form.instance.email)
            else:
                return super(MssgUpdateViewWithSubjectPk, self).form_invalid(form)
        return super(MssgUpdateViewWithSubjectPk, self).form_valid(form)

class SubjectListView(ListView):
    model = Subject
    form_class = MssgForm
    # success_url = reverse_lazy('mailing:Emails_list')
    # template_name = 'mailing/Mssg_list.html'
    # def get_context_data(self, request, pk, *args, **kwargs):
    #     context = super(MssgListView, self).get_context_data(**kwargs)
    #     context['something'] = Mssg.objects.filter(pk=self.kwargs.get('pk'))
    #     return context

class SubjectCreateView(CreateView):
    model = Mssg
    form_class = MssgForm
    # fields = '__all__'
    # success_url = reverse_lazy('mailing:Emails_list')
    # template_name = 'mailing/Mssg_list.html'
    def form_valid(self, form):###Zameniaem pole naimenovanie Subject na Naimenovanie polzovatelia
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.name = self.request.user
            self.object.save()
        return super(SubjectCreateView, self).form_valid(form)

class SubjectUpdateView(UpdateView):
    model = Mssg
    form_class = MssgForm
    # fields = '__all__'
    # success_url = reverse_lazy('mailing:Mssg_list_pk')
    # template_name = 'mailing/Mssg_list.html'
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


class MssgDetailView(DetailView):
    model = Mssg
    form_class = MssgForm
    success_url = reverse_lazy('mailing:Emails_list')
    fields = '__all__'
    template_name = 'mailing/Mssg_detail.html'
class MssgDeleteView(DeleteView):
    model = Mssg
    form_class = MssgForm
    success_url = reverse_lazy('mailing:Emails_list')
    template_name = ''

class EmailsDeleteView(DeleteView):
    model = Emails
    form_class = EmailsForm
    success_url = reverse_lazy('mailing:Emails_list')
    template_name = ''


class EmailsListView(ListView):
    model = Emails
    form_class = EmailsForm
    uccess_url = reverse_lazy('mailing:Emails_list')
    template_name = ''

class EmailsCreateView(CreateView):
    model = Emails
    form_class = EmailsForm
    success_url = reverse_lazy('mailing:Emails_list')
    template_name = 'mailing/Emails.html'

class EmailsUpdateVew(UpdateView):
    model = Emails
    form_class = EmailsForm
    success_url = reverse_lazy('mailing:Emails_list')
    template_name = 'mailing/Emails.html'


class EmailsDetailView(DetailView):
    model = Emails
    form_class = EmailsForm
    success_url = reverse_lazy('mailing:Emails_list')
    template_name = 'mailing/Emails.html'


# class ClientCreateView(CreateView):#Zapretili sozdanie producta
#     model = Client
#     # permission_required = 'catalog.create_Product'
#     #form_class = SubjectForm
#     form_class = ClientForm
#     # fields = ('product_name', 'product_description', 'preview', 'price_per_unit', 'category')
#     success_url = reverse_lazy('mailing:Client_list')
#     template_name = 'mailing/Client_list.html'
#
#
# class ClientUpdateView(UpdateView):#LoginRequiredMixin,
#     model = Client
#     # form_class = ClientForm
#     # success_url = reverse_lazy('catalog:Product_list')
#     template_name = 'mailing/Client_list.html'

#
# class ClientDeleteView(DeleteView):#UserPassesTestMixin,
#     model = Client
#     form_class = ClientForm
#     success_url = reverse_lazy('catalog:Product_list')
#     template_name = 'catalog/product_confirm_delete.html'
#
#     # def test_func(self):
#     #     return self.request.user.is_superuser
#
#
# class ClientDetailView(DetailView):#LoginRequiredMixin,
#     model = Client
#     # form_class = ProductForm
#     success_url = reverse_lazy('catalog:Product_list')
#     template_name = 'catalog/Product_detail.html'
#######################Primer sozdania formi dlia zapolnenia polya
# from django import forms
# from django.shortcuts import get_object_or_404
#
# class ItemForm(forms.ModelForm):
#     class Meta:
#         model = Item
#         fields = ("name", )
#
# def bound_form(request, id):
#     item = get_object_or_404(Item, id=id)
#     form = ItemForm(instance=item)
#     return render_to_response('bounded_form.html', {'form': form})