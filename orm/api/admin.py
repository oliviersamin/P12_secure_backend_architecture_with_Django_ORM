from django.contrib import admin
from .models import Client, Contract, Event, Sales, Support
from django.contrib import messages
from rest_framework import filters


class ClientsAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email']
    filter_backends = (filters.SearchFilter,)
    list_display = ('client_id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'is_confirmed_client',
                    'company_name', 'date_created')
    events = Event.objects.all()
    supports = [support.user for support in list(Support.objects.all())]

    def get_queryset(self, request):
        """
        If the user is a support person, it display only clients that are related to events managed by the user.
        If the user is not a support person, then he can see all the clients
        :param request:
        :return: QuerySet
        """
        qs = super().get_queryset(request)
        if request.user in self.supports:
            valid_clients_id = []
            for event in self.events:
                try:
                    if event.support.user == request.user:
                        valid_clients_id.append(event.contract.client.client_id)
                except AttributeError:
                    pass
            return qs.filter(client_id__in=valid_clients_id)
        return qs

    def message_user(self, *args):
        """
        override this method to cancel all the usual messages displayed when clicked on the save button
        :param args:
        :return:
        """
        pass

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
        existing_contracts = list(Contract.objects.filter(client_id=obj.client_id))
        existing_contracts = [contract.sales.user for contract in existing_contracts]
        # Step 2
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
            if not change:
                message = "Client créé avec succès"
            else:
                message = "Client modifié avec succès"
            messages.success(request, message)
        # Step 3
        elif not change:
            super().save_model(request, obj, form, change)
            message = "Client créé avec succès"
            messages.success(request, message)
        # Step 4
        else:
            if (existing_contracts != []) & (request.user in existing_contracts):
                super().save_model(request, obj, form, change)
                message = "Client modifié avec succès"
                messages.success(request, message)
            elif (request.user not in existing_contracts) & (existing_contracts != []):
                message = "Vous n'êtes pas autorisé à modifier les détails de ce client car" \
                          "vous n'avez signé aucun contrat avec lui."
                messages.error(request, message)
            else:
                super().save_model(request, obj, form, change)
                message = "Client modifié avec succès"
                messages.success(request, message)


class ContractsAdmin(admin.ModelAdmin):
    search_fields = ['client__first_name', 'client__last_name', 'client__email', 'date_created', 'amount']
    filter_backends = (filters.SearchFilter,)
    list_display = ('contract_id', 'signed', 'amount', 'payment_due', 'client', 'sales', 'date_created')

    def get_readonly_fields(self, request, obj=None):
        """
        Step 1: The superuser can get access and modify all the data
        Step2: If the sales user is the sales contact in the contract he can modify some data
        Step3: If the sales user is not the sales contact in the contract, he cannot change anything
        :param request:
        :param obj:
        :return:
        """
        user = request.user
        readonly = []
        if (user.is_superuser) or (obj is None):
            readonly = []
        elif user == obj.sales.user:
            readonly = ['client', 'sales', 'date_created']
        elif user != obj.sales.user:
            readonly = ['client', 'sales', 'date_created', 'signed', 'amount', 'payment_due',]
        return readonly

    def message_user(self, *args):
        """
        override this method to cancel all the usual messages displayed when clicked on the save button
        :param args:
        :return:
        """
        pass

    def save_model(self, request, obj, form, change):
        """
        Step 1: check that the client in the contract is a confirmed client
        Step 2: check if user is superuser so that he can perform all the actions he wants
        Step 3: check if this is the creation of a new contract
        Step 4: check if the update comes from a sales person which is not the sales contact
        Step 5: check if the update comes from a sales person which is the sales contact
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        # Step 1
        if obj.client.is_confirmed_client:
            # Step 2
            if request.user.is_superuser:
                super().save_model(request, obj, form, change)
                if change:
                    message = "contrat {} modifié avec succès".format(obj.contract_id)
                else:
                    message = "contrat {} créé avec succès".format(obj.contract_id)
                messages.success(request, message)
            # Step 3
            elif not change:
                if obj.sales.user == request.user:  # the sales contact correspond to the user of request
                    super().save_model(request, obj, form, change)
                    message = "contrat {} créé avec succès".format(obj.contract_id)
                    messages.success(request, message)
                else:  # the sales contact correspond to the user of request
                    message = "contrat non créé, vous devez être le contact de vente " \
                              "pour ce contrat".format(obj.contract_id)
                    messages.error(request, message)

            else:
                # Step 4
                if request.user != obj.sales.user:
                    message = "Opération non réalisée. Vous n'êtes pas autorisé à modifier " \
                              "le contrat {}".format(obj.contract_id)
                    messages.error(request, message)
                # Step 5
                else:
                    super().save_model(request, obj, form, change)
                    message = "contrat {} modifié avec succès".format(obj.contract_id)
                    messages.success(request, message)

        else:
            client_name = obj.client.first_name + " " + obj.client.last_name
            message = "Opération non réalisée. Le client {} n'est pas un client confirmé. Vous devez modifier " \
                      "son statut 'is confirmed client' avant de créer un contrat avec lui.".format(client_name)
            messages.error(request, message)


class EventsAdmin(admin.ModelAdmin):
    search_fields = ['contract__client__first_name', 'contract__client__last_name', 'contract__client__email',
                     'event_date']
    filter_backends = (filters.SearchFilter,)
    list_display = ('event_id', 'contract_id', 'support_id', 'support_name', 'client_id', 'client_name', 'event_date',
                    'attendees', 'event_performed')
    events = Event.objects.all()
    supports = [support.user for support in list(Support.objects.all())]

    def get_queryset(self, request):
        """
        If the user is a support person, it will display only events that he manages or has managed.
        Otherwise it displays all the events.
        :param request:
        :return:
        """
        qs = super().get_queryset(request)
        if request.user in self.supports:
            valid_events_id = []
            for event in self.events:
                try:
                    if event.support.user == request.user:
                        valid_events_id.append(event.event_id)
                except AttributeError:
                    pass
            return qs.filter(event_id__in=valid_events_id)
        return qs

    def get_readonly_fields(self, request, obj=None):
        """
        Step 1: The superuser can get access and modify all the data
        Step2: If the user is the support person, he can modify some data
        :param request:
        :param obj:
        :return:
        """
        user = request.user
        readonly = []
        try:
            if user == obj.support.user:
                readonly = ['contract', 'support', 'date_created']
            return readonly
        except AttributeError:
            return readonly

    def message_user(self, *args):
        """
        override this method to cancel all the usual messages displayed when clicked on the save button
        :param args:
        :return:
        """
        pass

    def save_model(self, request, obj, form, change):
        """
        Step1: check if user is superuser so that he can perform all the actions he wants
        Step2: Check if this is an event creation
        Step3: Check if this is un update and the event has not been performed yet
            Step4: Check if the contract linked with the event is signed
            Step5: check if the update comes from a support person which is not the support contact
            Step6: check that the support contact updating can't change the support contact
            and the contract in it.
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        try:
            existing_event = list(Event.objects.filter(event_id=obj.event_id))[0]
        except IndexError:
            existing_event = list(Event.objects.filter(event_id=obj.event_id))
        print("\n######## existing_event = {} #########\n".format(existing_event))
        # Step 1
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
            if change:
                message = "Évènement modifié avec succès"
            else:
                message = "Évènement créé avec succès"
            messages.success(request, message)
        # Step 2
        elif not existing_event:
            print("\n##### obj = {} ######\n".format(obj))
            if not obj.support:
                super().save_model(request, obj, form, change)
                message = "Évènement créé avec succès"
                messages.success(request, message)
            else:
                message = "Évènement non créé. Vous ne pouvez pas choisir un contact de support."
                messages.error(request, message)

        # Step 3
        elif not existing_event.event_performed:
            # Step 4
            if obj.contract.signed:
                # Step 5
                if obj.support.user != request.user:
                    message = "Opération non réalisée. Vous n'êtes pas autorisé à modifier cet évènement."
                    messages.error(request, message)
                # Step 6
                else:
                    if (obj.support == existing_event.support) & (obj.contract == existing_event.contract):
                        super().save_model(request, obj, form, change)
                        message = "Évènement modifié avec succès"
                        messages.success(request, message)

                    else:
                        message = "Opération non réalisée. Vous n'êtes pas autorisé à modifier ces paramètres."
                        messages.error(request, message)
            else:
                message = "Opération non réalisée. Le contrat lié à cet évènement n'est pas encore signé."
                messages.error(request, message)
        else:
            message = "Opération non réalisée. L'évènement à déjà eu lieu et ne peut plus être modifié."
            messages.error(request, message)


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