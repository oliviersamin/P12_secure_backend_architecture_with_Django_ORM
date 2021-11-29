from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    email = models.CharField(max_length=100, unique=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=250, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now_add=True, blank=True)
    is_confirmed_client = models.BooleanField(default=False)

    def __str__(self):
        name = self.first_name + " " + self.last_name
        displayed = "name: {} - is_confirmed_client: {} - phone: {} - email: {}".format(name, str(self.is_confirmed_client), self.phone, self.email)
        return displayed


class Sales(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        displayed = "name: {}".format(str(self.user))
        return displayed


class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True, blank=True)
    signed = models.BooleanField(default=False)
    amount = models.FloatField(blank=True)
    payment_due = models.DateTimeField(blank=True)
    sales = models.OneToOneField(Sales, on_delete=models.CASCADE)

    def __str__(self):
        displayed = "id: {} - client: {} - signed: {} - amount: {} - payment_due: {}".\
            format(str(self.contract_id), str(self.client), self.signed, str(self.amount),
                   self.payment_due)
        return displayed


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    event_performed = models.BooleanField(default=False)
    attendees = models.IntegerField(blank=True)
    event_date = models.DateTimeField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        displayed = "id: {} - contract: {} - date: {}".\
            format(str(self.event_id), str(self.contract), self.event_date)
        return displayed


class Support(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)

    def __str__(self):
        displayed = "name: {}".\
            format(str(self.user))
        return displayed

