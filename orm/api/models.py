from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
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
    contract_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)
    signed = models.BooleanField(default=False)
    amount = models.FloatField(blank=True)
    payment_due = models.DateTimeField(blank=True)
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


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    event_performed = models.BooleanField(default=False)
    attendees = models.IntegerField(blank=True)
    event_date = models.DateTimeField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        displayed = "id: {} - contract: {} - date: {}".\
            format(str(self.event_id), str(self.contract), self.event_date)
        return displayed

    def contract_id(self):
        """ used for admin site visualization """
        return str(self.contract.contract_id)

    def client_id(self):
        """ used for admin site visualization """
        return self.contract.client_id

    def client_name(self):
        return self.contract.client_name()

    class Meta:
        verbose_name_plural = "Events"


class Support(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)

    def __str__(self):
        displayed = "name: {}".format(str(self.user))
        return displayed

