from django.contrib import admin

from .models import RepoItem, RepoRequirement

@admin.register(RepoItem)
class RepoItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'status')
    
@admin.register(RepoRequirement)
class RepoItemAdmin(admin.ModelAdmin):
    readonly_fields = ('repos',)
