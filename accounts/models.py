# Django imports
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from fund.models.organizations import Organization
from fund.models.sponsorships import Sponsorship
from django.db import models
from setup.basemodel import TimeBaseModel
from datetime import datetime



class Gender(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MyAccountManager(BaseUserManager):
	def create_superuser(self, email, password=None):
		if not email:
			raise ValueError("Users must have an email address.")
		if "@" not in email and ".com" not in email:
			raise ValueError("Invalid email input")
		if len(password) < 8:
			raise ValueError("Password 8 must contain at least 8 characters")

		user = self.model(email=self.normalize_email(email))
		user.is_superuser = True
		user.is_admin = True
		user.is_active = True
		user.is_staff = True
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password):
		if not email:
			raise ValueError("Users must have an email address.")
		if "@" not in email and ".com" not in email:
			raise ValueError("Invalid email input")
		if len(password) < 8:
			raise ValueError("Password 8 must contain at least 8 characters")

		user = self.model(email=self.normalize_email(email))
		user.set_password(password)
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	profile = models.ImageField(null=True, blank=True)
	username = models.CharField(max_length=200, blank=True, null=True)
	phone_number = models.CharField(max_length=30, null=True, blank=100)
	full_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True, blank=True)
	gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
	

	organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
	sponsorship = models.ForeignKey(Sponsorship, on_delete=models.CASCADE, null=True, blank=True)
	
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
	last_login = models.DateTimeField(verbose_name="last joined", auto_now=True)
	

	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	objects = MyAccountManager()

	USERNAME_FIELD = "email"
	# REQUIRED_FIELDS = [" "]

	class Meta:
		verbose_name_plural = "Users"
		ordering = ["-id"]

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True
	
	

class UserVerificationCode(TimeBaseModel):
    code = models.CharField(max_length=6, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expires = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f"{self.user.email}-{self.code}"

    class Meta:
        verbose_name_plural = "Verification Codes"
        ordering = ["created_at"]

    def is_expired(self):
        return datetime.utcnow().hour > self.expires.hour + 2

    def get_duration(self):
        current_hour = datetime.utcnow().hour
        expired_hour = self.expires.hour
        return current_hour - 3 > expired_hour


class LoggedInUserDevices(TimeBaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="logged_in_user_user"
    )
    ip_address = models.GenericIPAddressField()
    os = models.CharField(max_length=255)
    browser = models.CharField(max_length=255)
    expires = models.DateTimeField(default=datetime.utcnow)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.full_name}-{self.ip_address}"

    def is_refresh_token_expired(self):
        return datetime.utcnow().day >= self.created_at.day + 1

    class Meta:
        ordering = ["created_at"]