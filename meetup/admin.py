import csv
import io

import django.forms as forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.shortcuts import redirect
from django.urls import path
from django.urls import reverse
from django.utils.html import format_html

from .forms import CsvImportForm
from .models import Meeting, MeetingCategories, Participant, GroupParticipants

admin.site.site_header = "Anwesenheitstool Dashboard"


class ParticipantAdminInline(admin.TabularInline):
    model = Participant
    extra = 0


class GroupParticipantsInlineAdmin(admin.StackedInline):
    model = GroupParticipants
    extra = 0


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'begin', 'end',
                    'category', 'created', 'show_firm_url', 'show_meeting_url')
    list_filter = ('name', 'date', 'category')
    fields = ('name', 'date', 'begin', 'end', 'category', 'show_firm_url','show_meeting_url')
    readonly_fields = ('show_firm_url','show_meeting_url')
    inlines = [ParticipantAdminInline, GroupParticipantsInlineAdmin]

    def get_fields(self, request, obj=None):
        """
        Hide all readonly_fields if we are on the create view
        """
        fields = list(super().get_fields(request, obj=obj))
        if obj is None:
            for field in self.readonly_fields:
                fields.remove(field)
        return fields

    def show_firm_url(self, obj):
        return format_html("<a href='{url}'>Download</a>", url=reverse('export', args=[obj.id]))

    def show_meeting_url(self, obj):
        return format_html("<a href='{url}'>Anmelden</a>", url=reverse('meeting_checkin', args=[obj.presence_registration_uuid]))

    show_firm_url.short_description = "participantlist"



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


class CustomGroupAdminForm(forms.ModelForm):
    """
    Make adding multiple users to a group easier

    Source: https://gist.github.com/Grokzen/a64321dd69339c42a184
    """
    users = forms.ModelMultipleChoiceField(label=get_user_model().Meta.verbose_name_plural,
                                           queryset=get_user_model().objects.all(),
                                           widget=FilteredSelectMultiple(get_user_model().Meta.verbose_name, False))

    class Meta:
        model = Group
        exclude = []

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)

        if self.instance and self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save(self, commit=True):
        group = super().save(commit=commit)

        if group.pk is not None:
            group.user_set.set(self.cleaned_data['users'])
            self.save_m2m()

        return group


class CustomGroupAdmin(GroupAdmin):
    form = CustomGroupAdminForm


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
