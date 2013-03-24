from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class Ranking(models.Model):
	rating = models.DecimalField(max_digits=21, decimal_places=15)
	num_wins = models.IntegerField()
	num_matches = models.IntegerField()
	user = models.OneToOneField(User)

class Match(models.Model):
	winner_id = models.IntegerField()
	looser_id = models.IntegerField()
	date = models.DateField(auto_now=False, auto_now_add=True)
	is_verified = models.BooleanField()

class RegistrationForm(forms.Form):
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())

	def save(self):
		data = self.cleaned_data
		user = User.objects.create_user(username=data['username'],
										email=data['email'],
		 								password=data['password'])
		user.save()