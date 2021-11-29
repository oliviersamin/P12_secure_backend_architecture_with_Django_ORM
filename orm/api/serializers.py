from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Client, Sales, Contract, Support, Event


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_id', 'first_name', 'last_name', 'email', 'mobile']
        extra_kwargs = {'client_id': {'read_only': True}}


class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['contract_id', 'client', 'sales', 'signed', 'amount', 'payment_due']
        extra_kwargs = {'contract_id': {'read_only': True}}


class ContractDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_id', 'event_date', 'event_performed', 'notes']
        extra_kwargs = {'event_id': {'read_only': True}}


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


#
# class ProjectDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Projects
#         fields = ['id', 'title', 'description', 'type', 'contributors', 'author']
#         extra_kwargs = {'id': {'read_only': True},
#                         'contributors': {'read_only': True},
#                         'author': {'read_only': True}}
