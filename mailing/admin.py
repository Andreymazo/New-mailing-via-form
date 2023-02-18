from django.contrib import admin

from mailing.models import Client, Mssg, Emails, Subject


# admin.site.register(Client)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

# admin.site.register(Mssg)
@admin.register(Mssg)
class MssgAdmin(admin.ModelAdmin):
    list_display = ("link", "text", "status", "period")
    # list_filter = ("text", "link")
    search_fields = ("text", "link")
    list_filter = ['link']


# admin.site.register(Emails)
@admin.register(Emails)
class EmailsAdmin(admin.ModelAdmin):
    list_display = ("comment", "email", "status_complete")
    list_filter = ["comment"]
# admin.site.register(Subject)
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "email_subj", "mssg_subj", "email", "text")
    list_filter = ["name"]