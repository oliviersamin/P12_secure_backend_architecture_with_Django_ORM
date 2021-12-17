from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    """ client model """
    client_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    email = models.EmailField(max_length=100, unique=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=250, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)
    is_confirmed_client = models.BooleanField(default=False)

    def __str__(self):
        name = self.first_name + " " + self.last_name
        displayed = "id: {} | name: {} ".format(self.client_id, name)
        return displayed

    class Meta:
        verbose_name_plural = "Clients"


class Sales(models.Model):
    """ sales model """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def user_details(self):
        """ used for admin interface visual"""
        return "id: {} | name: {}".format(self.user.id, self.user)

    def __str__(self):
        displayed = "id: {} | name: {}".format(self.user.id, str(self.user))
        return displayed


class Contract(models.Model):
    """ contract model """
    contract_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)
    signed = models.BooleanField(default=False)
    amount = models.FloatField(blank=True, null=True)
    payment_due = models.DateTimeField(blank=True, null=True)
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE)

    def client_id(self):
        """ used for admin site visualization """
        return str(self.client.client_id)

    def client_name(self):
        """ used for admin site visualization """
        name = self.client.first_name + " " + self.client.last_name
        return name

    def __str__(self):
        displayed = "contract_id: {} - client_details: {} ".format(str(self.contract_id), str(self.client))
        return displayed

    class Meta:
        verbose_name_plural = "Contracts"


class Support(models.Model):
    """ support model """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def user_details(self):
        """ used for admin interface visual"""
        return "id: {} | name: {}".format(self.user.id, self.user)

    def __str__(self):
        displayed = "id: {} | name: {}".format(self.user.id, str(self.user))
        return displayed


class Event(models.Model):
    """ event model """
    event_id = models.AutoField(primary_key=True)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    event_performed = models.BooleanField(default=False)
    attendees = models.IntegerField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    support = models.ForeignKey(Support, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        displayed = "id: {} - contract: {} - date: {}".\
            format(str(self.event_id), str(self.contract), self.event_date)
        return displayed

    def contract_id(self):
        """ used for admin site visualization """
        return str(self.contract.contract_id)

    def client_id(self):
        """ used for admin site visualization """
        client_id = None
        try:
            client_id = self.contract.client_id
        except AttributeError:
            pass
        return client_id

    def client_name(self):
        client_name = None
        try:
            client_name = self.contract.client_name()
        except AttributeError:
            pass
        return client_name

    def support_id(self):
        """ used for admin site visualization """
        user_id = -1
        try:
            user_id = self.support.user.id
        except AttributeError:
            pass
        return user_id

    def support_name(self):
        """ used for admin site visualization """
        user_name = "To be assigned"
        try:
            user_name = self.support.user
        except AttributeError:
            pass
        return user_name


    class Meta:
        verbose_name_plural = "Events"



