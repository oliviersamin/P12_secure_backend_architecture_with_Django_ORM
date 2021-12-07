from django.contrib import admin
from .models import Client, Contract, Event, Sales, Support
from django.contrib import messages
from rest_framework import filters


class ClientsAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email']
    filter_backends = (filters.SearchFilter,)
    list_display = ('client_id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'is_confirmed_client',
                    'company_name', 'date_created')
    contracts = Contract.objects.all()
    def save_model(self, request, obj, form, change):
        """
        Step 1: check if there are contracts (even not signed) with this client.
        Step 2: any superuser can change anything anytime about the client
        Step 3: if there are not, then any sales can change the client details
        Step 4: if there are, then only the sales that have signed contracts can change the client details
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        # Step 1
        existing_contracts = []
        for contract in self.contracts:
            if contract.client.client_id == obj.client_id:
                existing_contracts.append(contract.sales.user)
        # Step 2
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
        # Step 3
        elif not existing_contracts:
            super().save_model(request, obj, form, change)
        # Step 4
        elif (existing_contracts != []) & (request.user in existing_contracts):
            super().save_model(request, obj, form, change)
        elif (existing_contracts != []) & (request.user not in existing_contracts):
            message = "Opération non réalisée. Vous n'êtes pas autorisé à modifier les détails de ce client car" \
                      "vous n'avez signé aucun contrat avec lui."
            self.message_user(request, message, messages.ERROR)


class ContractsAdmin(admin.ModelAdmin):
    search_fields = ['client__first_name', 'client__last_name', 'client__email', 'date_created', 'amount']
    filter_backends = (filters.SearchFilter,)
    list_display = ('contract_id', 'signed', 'amount', 'payment_due', 'client', 'sales', 'date_created')
    contracts = Contract.objects.all()

    def save_model(self, request, obj, form, change):
        """
        Step1: check if the contract is already existing and save it in case in the existing_contract variable
        Step2: check that the client in the contract is a confirmed client
        Step3: check if user is superuser so that he can perform all the actions he wants
        Step4: check if this is the creation of a new contract
        Step 5: check if the update comes from a sales person which is not the sales contact
        Step 6: check if this is an update of an existing contract and make sure that the sales contact updating
        it can't change the sales contact in it.
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        # Step 1
        existing_contract = None
        for contract in self.contracts:
            if contract.contract_id == obj.contract_id:
                existing_contract = contract
                break
        # Step 2
        if obj.client.is_confirmed_client:
            # Step 3
            if request.user.is_superuser:
                super().save_model(request, obj, form, change)
            # Step 4
            elif existing_contract is None:
                if obj.sales.user == request.user:
                    super().save_model(request, obj, form, change)
            # Step 5
            elif existing_contract is not None:
                if request.user != existing_contract.sales.user:
                    message = "Opération non réalisée. Vous n'êtes pas autorisé à modifier ce contrat"
                    self.message_user(request, message, messages.ERROR)
                # Step 6
                else:
                    if obj.sales.user == request.user:
                        super().save_model(request, obj, form, change)
                    else:
                        message = "Opération non réalisée. Vous n'êtes pas autorisé à modifier le contact de vente"
                        self.message_user(request, message, messages.ERROR)

            else:
                message = "Opération non réalisée. Vous êtes {} alors que {} est sélectionné comme contact de vente."\
                    .format(request.user, obj.sales.user)
                self.message_user(request, message, messages.ERROR)
        else:
            client_name = obj.client.first_name + " " + obj.client.last_name
            message = "Opération non réalisée. Le client {} n'est pas un client confirmé. Vous devez modifier " \
                      "son statut 'is confirmed client' avant de créer un contrat avec lui.".format(client_name)
            self.message_user(request, message, messages.ERROR)


class EventsAdmin(admin.ModelAdmin):
    search_fields = ['contract__client__first_name', 'contract__client__last_name', 'contract__client__email',
                     'event_date']
    filter_backends = (filters.SearchFilter,)
    list_display = ('event_id', 'contract_id', 'support_id', 'support_name', 'client_id', 'client_name', 'event_date', 'attendees', 'event_performed')
    events = Event.objects.all()

    def save_model(self, request, obj, form, change):
        """
        Step1: Check if the contract linked with the event is signed
        Step2: check if user is superuser so that he can perform all the actions he wants
        Step3: check if this is the creation of a new event
        Step4: check if the update comes from a support person which is not the support contact
        Step5: check if this is an update of an existing event and make sure that the support contact updating
        it can't change the support contact in it.
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        existing_event = None
        for event in self.events:
            if event.event_id == obj.event_id:
                existing_event = event
                break
        # Step 1
        if obj.contract.signed:
            # Step 2
            if request.user.is_superuser:
                super().save_model(request, obj, form, change)
            # Step 3
            elif obj.event_id != existing_event.event_id:
                super().save_model(request, obj, form, change)
            elif obj.event_id == existing_event.event_id:
                # Step 4
                if obj.support.user != request.user:
                    message = "Opération non réalisée. Vous n'êtes pas autorisé à modifier cet évènement."
                    self.message_user(request, message, messages.ERROR)
                # Step 5
                else:
                    if (obj.support == existing_event.support) & (obj.contract == existing_event.contract):
                        super().save_model(request, obj, form, change)
                    else:
                        message = "Opération non réalisée. Vous n'êtes pas autorisé à modifier ces paramètres."
                        self.message_user(request, message, messages.ERROR)

            else:
                message = "Opération non réalisée. Vous n'êtes pas autorisé à faire cette modification."
                self.message_user(request, message, messages.ERROR)
        else:
            message = "Opération non réalisée. Le contrat lié à cet évènement n'es pas encore signé." \
                      "Le contrat doit être signé avant de pouvoir créer un évènement."
            self.message_user(request, message, messages.ERROR)



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