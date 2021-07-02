from django.contrib import admin
from .models import Meeting, MeetingCategories, Participant

admin.site.site_header = "Anwesenheitstool Dashboard"


class ParticipantAdminInline(admin.TabularInline):
    model = Participant


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'begin', 'end', 'category', 'created')
    list_filter = ('name', 'date', 'category')
    model = Meeting
    inlines = [ParticipantAdminInline]


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MeetingCategories)
