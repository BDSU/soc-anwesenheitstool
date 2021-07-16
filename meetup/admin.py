import csv
import io

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.forms import forms
from django.shortcuts import redirect, render
from django.urls import path
from django.contrib.auth.models import User

from .models import Meeting, MeetingCategories, Participant, GroupParticipants
from .forms import CsvImportForm

admin.site.site_header = "Anwesenheitstool Dashboard"


class ParticipantAdminInline(admin.TabularInline):
    model = Participant
    extra = 0


class GroupParticipantsInlineAdmin(admin.StackedInline):
    model = GroupParticipants
    extra = 0


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'begin', 'end', 'category', 'created')
    list_filter = ('name', 'date', 'category')
    fields = ('name', 'date', 'begin', 'end', 'category')
    inlines = [ParticipantAdminInline, GroupParticipantsInlineAdmin]


@admin.register(MeetingCategories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


# Unregister the provided model admin
admin.site.unregister(User)


# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CsvUploadAdmin(UserAdmin):
    change_list_template = "admin/csv_form.html"

    def get_urls(self):
        urls = super().get_urls()
        additional_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return additional_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra = extra_context or {}
        extra['csv_upload_form'] = CsvImportForm()
        return super(CsvUploadAdmin, self).changelist_view(request, extra_context=extra)

    def upload_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                self.handle_csv_request(request)
        return redirect("..")

    def handle_csv_request(self, request):
        if request.FILES['csv_file'].name.endswith('csv'):

            try:
                decoded_file = request.FILES['csv_file'].read().decode('utf-8-sig')
            except UnicodeDecodeError as e:
                self.message_user(
                    request,
                    "There was an error decoding the file:{}".format(e),
                    level=messages.ERROR
                )
                return
            file = io.StringIO(decoded_file)
            self.handle_user_creation(file)

    def handle_user_creation(self, csv_file):
        """Handle CSV Data in Form:
        ID; Username; first_name; last_name; email; password
        The file has no header and a delimiter of ;
        """
        data = csv.DictReader(csv_file, delimiter=',')

        # userPrincipalName
        # displayName
        # surname
        # mail
        # givenName
        # id
        # userType
        # jobTitle
        # department
        # accountEnabled
        # usageLocation
        # streetAddress
        # state
        # country
        # officeLocation
        # city
        # postalCode
        # telephoneNumber
        # mobilePhone
        # alternateEmailAddress
        # ageGroup
        # consentProvidedForMinor
        # legalAgeGroupClassification
        # companyName
        # creationType
        # directorySynced
        # invitationState
        # identityIssuer
        # createdDateTime

        User.objects.bulk_create([
            User(
                username=row['userPrincipalName'],
                first_name=row['givenName'],
                last_name=row['surname'],
                email=row['mail'],
                # password=row[5],
                is_staff=False,
            ) for row in data
        ])
