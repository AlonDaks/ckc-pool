from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.forms import ModelForm
from django import forms

class RegistrationForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def save(self):
        data = self.cleaned_data
        user = MyUser.objects.create_user(email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password'])
        user.save()
        ranking_data = Ranking(user=user, rating=1500, num_wins=0, num_matches=0)
        ranking_data.save()

    def clean_password(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            return False
        return password2

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
 
        user = self.model(
            email=MyUserManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, twitter_handle, password):
        user = self.create_user(email,
            password=password,
            twitter_handle=twitter_handle,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
     


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
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

class Ranking(models.Model):
    user = models.OneToOneField(MyUser, primary_key=True)
    rating = models.DecimalField(max_digits=15, decimal_places=11)
    num_wins = models.IntegerField()
    num_matches = models.IntegerField()

class Match(models.Model):
    winner_id = models.IntegerField()
    looser_id = models.IntegerField()
    date = models.DateField(auto_now=False, auto_now_add=True)
    is_verified = models.BooleanField()            

class MatchEntryForm(forms.Form):
    winner_email = forms.EmailField()
    looser_email = forms.EmailField()

    @property
    def winner_id(self):
        return MyUser.objects.get(email=self.cleaned_data['winner_email']).id

    @property
    def looser_id(self):
        return MyUser.objects.get(email=self.cleaned_data['looser_email']).id

    def save(self):
        data = self.cleaned_data
        winner_email = data['winner_email']
        looser_email = data['looser_email']
        winner = MyUser.objects.get(email=winner_email)
        looser = MyUser.objects.get(email=looser_email)
        match = Match(winner_id=winner.id, looser_id=looser.id)
        match.save()





