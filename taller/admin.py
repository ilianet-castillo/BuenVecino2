from django.contrib import admin
from django.urls import path

from . import views
from .models import *


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ['name', 'email', 'phone']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'title')
    search_fields = ['title']


@admin.register(UnitMeasurement)
class UnitMeasurementAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ['name', 'phone']


@admin.register(Mechanical)
class MechanicalAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name')
    list_filter = ['name']
    search_fields = ['name', 'last_name']


@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(MethodPayment)
class MethodPaymentAdmin(admin.ModelAdmin):
    search_fields = ['type']


@admin.register(ServiceGuarantee)
class ServiceGuaranteeAdmin(admin.ModelAdmin):
    search_fields = ['description']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('tag', 'model', 'mark', 'enterprise')
    search_fields = ['tag', 'model', 'mark', 'enterprise__name']


@admin.register(PhysicalState)
class PhysicalStateAdmin(admin.ModelAdmin):
    list_display = ('piece', 'description')
    search_fields = ['description', 'workshop_order__entry_date']


class PhysicalStateTabularInline(admin.TabularInline):
    model = PhysicalState
    extra = 0


@admin.register(WorkshopOrder)
class WorkshopOrderAdmin(admin.ModelAdmin):
    list_display = ('entry_date', 'enterprise', 'vehicle', 'mechanical')
    inlines = [PhysicalStateTabularInline]
    change_form_template = "admin/show_order_workshop.html"

    def get_urls(self):
        urls = [
            path('<path:object_id>/export_pdf', views.export_workshop_order_pdf,
                 name='taller_order_workshop_export_pdf'),
        ]

        return super().get_urls() + urls


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'code', 'provenance')
    search_fields = ['invoice__pk', 'code', 'provenance__provenance']


class ActivityTabularInline(admin.TabularInline):
    model = Activity
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('type', 'date', 'contact', 'workshop_order')
    list_filter = ['date']
    search_fields = ['type__title', 'date', 'contact__name', 'workshop_order__pk']
    inlines = [ActivityTabularInline]
    change_form_template = "admin/show_invoice.html"

    def get_urls(self):
        urls = [
            path('<path:object_id>/export_pdf', views.export_invoice_pdf, name='taller_invoice_export_pdf'),
        ]

        return super().get_urls() + urls


@admin.register(Provenance)
class Provenance(admin.ModelAdmin):
    search_fields = ['provenance']
