from rest_framework.permissions import BasePermission


class IsClientContact(BasePermission):
    """
    Used for Sales to get permission to update data on a client
    Step 1: check if the client is confirmed
        - if no, it means than no contract has been signed yet and anyone can change its data
        - if yes go to step 2
    Step 2: check if the client has signed a contract
        - if not then any sales can update the client details
        - if yes then only the sales that have signed the contract with the client can change its details
    """
    def has_object_permission(self, request, view, obj):
        """
        :param request:
        :param view:
        :param obj:
        :return: boolean:
        """
        # Step 1
        if obj.is_confirmed_client:
            # Step 2
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


class IsSalesContact(BasePermission):
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
        if obj.sales.user == request.user:
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