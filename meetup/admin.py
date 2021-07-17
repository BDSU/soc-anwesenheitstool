import django.forms as forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.forms.utils import ErrorList
from django.urls import reverse
from django.utils.html import format_html

from .models import Meeting, MeetingCategories, Participant, GroupParticipants

admin.site.site_header = "Anwesenheitstool Dashboard"


class ParticipantAdminInline(admin.TabularInline):
    model = Participant
    extra = 0


class GroupParticipantsInlineAdmin(admin.StackedInline):
    model = GroupParticipants
    extra = 0


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'begin', 'end',
                    'category', 'created', 'show_firm_url', 'show_meeting_url')
    list_filter = ('name', 'date', 'category')
    fields = ('name', 'date', 'begin', 'end', 'category', 'show_firm_url','show_meeting_url')
    readonly_fields = ('show_firm_url','show_meeting_url')
    model = Meeting
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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    model = MeetingCategories


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MeetingCategories, CategoryAdmin)


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
