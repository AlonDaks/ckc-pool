from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.forms import ModelForm
from django import forms

# class Ranking(models.Model):
# 	rating = models.DecimalField(max_digits=21, decimal_places=15)
# 	num_wins = models.IntegerField()
# 	num_matches = models.IntegerField()
# 	user = models.OneToOneField(User)

class Match(models.Model):
	winner_id = models.IntegerField()
	looser_id = models.IntegerField()
	date = models.DateField(auto_now=False, auto_now_add=True)
	is_verified = models.BooleanField()	

class RegistrationForm(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())

	def save(self):
		data = self.cleaned_data
		user = MyUserManager().create_user(email=data['email'],
			first_name=data['first_name'],
			last_name=data['last_name'],
			password=data['password'])
		user.save()


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
        	raise ValueError('Users must have a first name')
        if not last_name:
        	raise ValueError('Users must have a last name')
 
        # user = self.model(
        #     email=MyUserManager.normalize_email(email),
        #     first_name=first_name,
        #     last_name=last_name
        # )
 
 		user = self.model(
            email="Alon.daks@gmail.com",
            first_name="alon",
            last_name="daks"
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    #rating = models.DecimalField(max_digits=15, decimal_places=11)
 
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
 
    objects = MyUserManager()
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
 
    def get_full_name(self):
        # For this case we return email. Could also be User.first_name User.last_name if you have these fields
        return self.first_name + " " + self.last_name
 
    def get_short_name(self):
        # For this case we return email. Could also be User.first_name if you have this field
        return self.first_name
 
    def __unicode__(self):
        return self.email
 
    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?"
        return True
 
    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?"
        return True
 
    @property
    def is_staff(self):
        # Handle whether the user is a member of staff?"
        return self.is_admin
    # def create_superuser(self, email, twitter_handle, password):
    #     user = self.create_user(email,
    #         password=password,
    #         twitter_handle=twitter_handle,
    #     )
    #     user.is_admin = True
    #     user.save(using=self._db)
    #     return user
 