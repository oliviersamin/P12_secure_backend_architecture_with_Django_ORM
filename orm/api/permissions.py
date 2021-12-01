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
            if (contract.sales.user == request.user) & (contract.client == obj):
                return True
        return False


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
        for support in view.supports:
            if (support.event == obj) & (request.user == support.user):
                return True
        return False