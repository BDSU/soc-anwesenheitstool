from django.contrib import admin
from .models import Meeting, MeetingCategories, Participant, GroupParticipants
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect, render

admin.site.site_header = "Anwesenheitstool Dashboard"


class ParticipantAdminInline(admin.TabularInline):
    model = Participant
    extra = 0


class GroupParticipantsInlineAdmin(admin.StackedInline):
    model = GroupParticipants
    extra = 0


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'begin', 'end',
                    'category', 'created', 'show_firm_url')
    list_filter = ('name', 'date', 'category')
    fields = ('name', 'date', 'begin', 'end', 'category', 'show_firm_url',)
    readonly_fields = ('show_firm_url',)
    model = Meeting
    inlines = [ParticipantAdminInline, GroupParticipantsInlineAdmin]

    def show_firm_url(self, obj):
        return format_html("<a href='{url}'>Download</a>", url=reverse('export', args=[obj.id]))
        # return format_html("<a href='{url}'>Download</a>", url="http://127.0.0.1:8000/export/" + str(obj.id))

    show_firm_url.short_description = "participantlist"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    model = MeetingCategories


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MeetingCategories, CategoryAdmin)
