from django.contrib import admin
from .models import Client, Contract, Event, Sales, Support


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'is_confirmed_client',
                    'company_name', 'date_created')


class ContractsAdmin(admin.ModelAdmin):
    list_display = ('contract_id', 'signed', 'amount', 'payment_due', 'client', 'sales', 'date_created')


class EventsAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'contract_id', 'client_id', 'client_name', 'event_date', 'attendees', 'event_performed')


class SalesAdmin(admin.ModelAdmin):
    list_display = ('user_details', 'phone', 'mobile', 'date_updated', 'date_created')

class SupportAdmin(admin.ModelAdmin):
    # list_display = ('event_id', 'contract', 'event_date', 'attendees', 'event_performed')
    pass

admin.site.register(Client, ClientsAdmin)
admin.site.register(Contract, ContractsAdmin)
admin.site.register(Event, EventsAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(Support, SupportAdmin)