from django.db import models

class Ranking(models.Model):
	rating = models.DecimalField(max_digits=21, decimal_places=15)


# class Match(models.Model):

# class User(models.Model):

