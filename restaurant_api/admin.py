from django.contrib import admin
from restaurant_api.models import Check, Printer


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_filter = ("printer", "type", "status")


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    pass
