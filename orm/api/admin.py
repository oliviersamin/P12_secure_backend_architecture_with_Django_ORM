from django.contrib import admin
from .models import Client, Contract, Event, Sales, Support
from django.contrib import messages



class ClientsAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'is_confirmed_client',
                    'company_name', 'date_created')


class ContractsAdmin(admin.ModelAdmin):
    list_display = ('contract_id', 'signed', 'amount', 'payment_due', 'client', 'sales', 'date_created')

    def save_model(self, request, obj, form, change):
        print("#### SAVE_MODEL #########")
        print("client.is_confirmed: ", obj.client.is_confirmed_client)
        print("sales_id: ", obj.sales.user.id)
        print("obj.sales.user == request.user ", obj.sales.user == request.user)
        print("obj.client.is_confirmed_client ", obj.client.is_confirmed_client)
        if obj.client.is_confirmed_client:
            if obj.sales.user == request.user:
                super().save_model(request, obj, form, change)
            else:
                message = "ERREUR: Contrat non créé. Le contact de vente ne correspond à votre identité."
                self.message_user(request, message, messages.ERROR)
        else:
            message = "ERREUR: Contrat non créé. Le client choisi n'est pas un client confirmé." \
                      "Vous devez modifier son statut is_confirmed_client avant de créér un contrat avec lui."
            self.message_user(request, message, messages.ERROR)


class EventsAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'contract_id', 'support_id', 'support_name', 'client_id', 'client_name', 'event_date', 'attendees', 'event_performed')


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