from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255)
    age = models.SmallIntegerField()
    company = models.ForeignKey('Company', models.CASCADE)


class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
