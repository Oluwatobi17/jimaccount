from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	role = models.CharField(max_length=10, default='read')

	def __str__(self):
		return self.username


class Investment(models.Model):
	investor = models.ForeignKey(User, on_delete=models.CASCADE)
	interest_rate = models.IntegerField()
	amount = models.IntegerField()
	investmentDate = models.DateTimeField()

class Capitallog(models.Model):
	title = models.CharField(max_length=1000)


class Account(models.Model):
	log = models.ForeignKey(Capitallog, on_delete=models.CASCADE)
	amount = models.IntegerField()
	accType = models.CharField(max_length=10)
	description = models.CharField(max_length=1000)

	author = models.ForeignKey(User, on_delete=models.CASCADE)