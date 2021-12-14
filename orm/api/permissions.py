from rest_framework.permissions import BasePermission
from api.models import Client, Support, Sales, Event, Contract


class ClientsPermissions(BasePermission):
    """
    Used for Sales to get permission to update data on a client
    Step 1: check if the user is a support person
    Step 2: check if the client is confirmed
        - if no, it means than no contract has been signed yet and anyone can change its data
        - if yes go to step 2
    Step 3: check if the client has signed a contract
        - if not then any sales can update the client details
        - if yes then only the sales that have signed the contract with the client can change its details
    """
    supports = Support.objects.all()
    supports = [support.user for support in supports]

    def has_permission(self, request, view):
        """
        Authorize only Sales person to create or update clients data
        :param request:
        :param view:
        :return:
        """
        methods = ["POST", "PUT", "PATCH"]
        if (request.user in self.supports) & (request.method in methods):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        """
        :param request:
        :param view:
        :param obj:
        :return: boolean:
        """
        # Step 1 to authorize all GET requests to be performed by supports person
        if request.user in self.supports:
            return True
        # Step 2
        elif obj.is_confirmed_client:
            # Step 3
            contract_signed = False
            client_with_contract = []
            for contract in view.contracts:
                if contract.client == obj:
                    contract_signed = True
                    break
            if contract_signed:
                for contract in view.contracts:
                    if contract.client == obj:
                        client_with_contract.append(contract)
                if client_with_contract:
                    for contract in client_with_contract:
                        if contract.sales.user == request.user:
                            return True
                return False
            return True
        else:
            return True


class ContractsPermissions(BasePermission):
    """
    Used to grant permissions to Sales person only
    """
    def has_permission(self, request, view):
        """

        :param request:
        :param view:
        :return:
        """
        supports = Support.objects.all()
        supports = [support.user for support in supports]
        if request.user in supports:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        """
        check if the user is the sales contact of the contract
            - if yes all requests are granted (appart from delete)
            - else GET request only
        :param request:
        :param view:
        :param obj:
        :return: boolean:
        """
        print("\n######## has obj perm ##########")
        print(obj.sales.user)
        print(request.user)
        print(obj.sales.user == request.user)
        if (obj.sales.user == request.user) & (request.method in ["POST", "PUT", "PATCH"]):
            return True
        elif request.method == "GET":
            return True
        return False


class EventsPermissions(BasePermission):
    """
    Used to grant GET and POST permissions to Sales person and GET and PUT permissions to
    support persons
    """
    supports = Support.objects.all()
    supports = [support.user for support in supports]
    sales = Sales.objects.all()
    sales = [sale.user for sale in sales]
    methods_sales = ["GET", "POST"]
    methods_supports = ["GET", "PUT"]

    def has_permission(self, request, view):
        """
        :param request:
        :param view:
        :return:
        """
        if (request.user in self.supports) & (request.method in self.methods_supports):
            return True
        elif (request.user in self.sales) & (request.method in self.methods_sales):
            return True
        return False


class IsEventContact(BasePermission):
    """
    Used for Sales to get permission to update data on a client
    """
    def has_object_permission(self, request, view, obj):
        """
        :param request:
        :param view:
        :param obj:
        :return: boolean:
        """
        # for support in view.supports:
        try:
            if (request.user == obj.support.user):
                return True
        except AttributeError:
            pass
        return False