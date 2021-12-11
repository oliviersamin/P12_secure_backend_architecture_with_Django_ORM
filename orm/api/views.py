# from django.shortcuts import render
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import ClientSerializer, ClientDetailSerializer, ContractSerializer, ContractDetailSerializer
from api.serializers import EventSerializer, EventDetailSerializer
from api.models import Client, Support, Sales, Event, Contract
from rest_framework.permissions import DjangoModelPermissions
from api.permissions import IsClientContact, IsSalesContact, IsEventContact


class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Logout performed successfully")


class ClientsViewset(ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    search_fields = ['first_name', 'last_name', 'email']
    filter_backends = (filters.SearchFilter,)
    serializer_class = ClientSerializer
    detail_serializer_class = ClientDetailSerializer
    contracts = Contract.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsClientContact,]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Client.objects.all()

    def get_serializer_class(self):
        if self.action not in ['list', 'delete']:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContractsViewset(ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    search_fields = ['client__first_name', 'client__last_name', 'client__email', 'date_created', 'amount']
    filter_backends = (filters.SearchFilter,)
    serializer_class = ContractSerializer
    detail_serializer_class = ContractDetailSerializer
    sales_persons = Sales.objects.all()

    def create(self, request, *args, **kwargs):
        """ generate automatically that:
         1. salesman linked to the contract is the one creating the contract
         2. the contract can be created only if the client_isconfirmed_client is set to True"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.validated_data['client']
        instance = None
        if client.is_confirmed_client:
            for sale in self.sales_persons:
                if sale.user == request.user:
                    instance = serializer.save(sales=sale)
                    break
            return_serializer = self.detail_serializer_class(instance)
            headers = self.get_success_headers(return_serializer.data)
            return Response(
                return_serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            message = "CONTRACT NOT CREATED: The selected client is not confirmed, please change the " \
                      "is_confirmed_client status of the client to be able to create the contract"
            return Response(message, status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        return Contract.objects.all()

    def get_serializer_class(self):
        if self.action not in ['list', 'delete']:
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsSalesContact,]
        return [permission() for permission in permission_classes]


class EventsViewset(ModelViewSet):
    # supports = Support.objects.all()
    permission_classes = (DjangoModelPermissions,)
    search_fields = ['contract__client__first_name', 'contract__client__last_name', 'contract__client__email',
                     'event_date']
    filter_backends = (filters.SearchFilter,)
    serializer_class = EventSerializer
    detail_serializer_class = EventDetailSerializer

    def create(self, request, *args, **kwargs):
        """ generate automatically that:
         1. the event can be created only if the signed attribute of the contract is set to True"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contract = serializer.validated_data['contract']
        print("\n###### CREATE EVENT ###########")
        print(serializer.validated_data.keys())
        if contract.signed:
            instance = serializer.save()
            return_serializer = self.detail_serializer_class(instance)
            headers = self.get_success_headers(return_serializer.data)
            return Response(
                return_serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            message = "EVENT NOT CREATED: The selected contract is not signed, please change the " \
                      "signed status of the contract to be able to create the event"
            return Response(message, status=status.HTTP_403_FORBIDDEN)


    def get_queryset(self):
        return Event.objects.all()

    def get_serializer_class(self):
        if self.action not in ['list', 'delete']:
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsEventContact,]
        return [permission() for permission in permission_classes]
