from rest_framework.permissions import BasePermission


class IsClientContact(BasePermission):
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
        for contract in view.contracts:
            print(contract.sales.user, request.user, contract.sales.user == request.user)
            if (contract.sales.user == request.user) & (contract.client == obj):
                return True
        return False