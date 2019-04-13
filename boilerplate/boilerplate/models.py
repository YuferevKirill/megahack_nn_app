from django.db import models as md
from django.contrib.postgres import fields as pg


class SexChoices:
    MALE = 'M'
    FEMALE = 'F'
    NONBINARY = 'NB'
    CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NONBINARY, 'Nonbinary')
    )


class SourceTypeChoices:
    SQL = 'SQL'
    REDIS = 'REDIS'
    HTTP = 'HTTP'
    CHOICES = (
        (SQL, 'SQL'),
        (REDIS, 'Redis'),
        (HTTP, 'HTTP')
    )


class Source(md.Model):
    database = md.CharField(max_length=100, null=True)
    name = md.CharField(max_length=100, null=False)
    port = md.IntegerField(null=False)
    host = md.CharField(max_length=100, null=False)
    username = md.CharField(max_length=100, null=False)
    password = md.CharField(max_length=100, null=False)
    type = md.CharField(max_length=10, choices=SourceTypeChoices.CHOICES)


# Диллер, продающий симкарты и предлагающий акции
class Dealer(md.Model):
    name = md.CharField(max_length=100, null=False, unique=True)


class Client(md.Model):
    name = md.CharField(max_length=100, null=False)
    date_of_admission = md.DateTimeField(auto_now=True)
    sex = md.CharField(max_length=100, null=True, choices=SexChoices.CHOICES)
    phone = md.CharField(max_length=10, null=False)
    age = md.IntegerField(null=False)
    dealer = md.ForeignKey(Dealer, on_delete=md.SET_NULL, null=True)


# Акция, которую предлагают абоненту
class Offer(md.Model):
    name = md.CharField(max_length=100, null=False, unique=True)
    due_date = md.DateTimeField(default=None, null=True)
    options = pg.JSONField(null=True)


# Критерии по которым определяется подходит ли акция абоненту
class Options(md.Model):
    options = pg.JSONField(null=False)


class OfferOrderResultChoices:
    SUCCESS = 'Success'
    FAIL = 'Fail'
    PENDING = 'Pending'
    CHOICES = (
        (SUCCESS, 'S'),
        (FAIL, 'F'),
        (PENDING, 'P')
    )


class OfferOrder(md.Model):
    offer = md.ForeignKey(Offer, on_delete=md.CASCADE)
    client = md.ForeignKey(Client, on_delete=md.CASCADE)
    dealer = md.ForeignKey(Dealer, on_delete=md.SET_NULL, null=True)
    id_hash = md.CharField(max_length=64)
    result = md.CharField(max_length=3, choices=OfferOrderResultChoices.CHOICES)
    date_created = md.DateTimeField(auto_now=True)
    date_processed = md.DateTimeField(null=True, default=None)
