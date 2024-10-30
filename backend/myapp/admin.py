from django.contrib import admin

from myapp.models import CaughtMessage, Pattern


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    pass


@admin.register(CaughtMessage)
class CaughtMessageAdmin(admin.ModelAdmin):
    pass
