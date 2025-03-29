from django.contrib import admin
from .models import Status, Issue

class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'status', 'priority', 'reporter', 'assignee', 'created_on')
    list_filter = ('status', 'created_on')
    search_fields = ('name', 'summary', 'description', 'priority')
    raw_id_fields = ('reporter', 'assignee')
    date_hierarchy = 'created_on'
    
admin.site.register(Issue, IssueAdmin)