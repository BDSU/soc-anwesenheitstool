from django.contrib import admin
from .models import Meeting, MeetingCategories, Participant, GroupParticipants

admin.site.site_header = "Anwesenheitstool Dashboard"


class ParticipantAdminInline(admin.TabularInline):
    model = Participant
    extra = 0


class GroupParticipantsInlineAdmin(admin.StackedInline):
    model = GroupParticipants
    extra = 0


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'begin', 'end', 'category', 'created')
    list_filter = ('name', 'date', 'category')
    fields = ('name', 'date', 'begin', 'end', 'category')
    model = Meeting
    inlines = [ParticipantAdminInline, GroupParticipantsInlineAdmin]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    model = MeetingCategories


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MeetingCategories, CategoryAdmin)
