from email.policy import default
from io import BytesIO
from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image


# ....................CUSTOM USER MODEL...........................
class AccountManager(BaseUserManager):

    def create_superuser(self, first_name, last_name, contact_number, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_contact_number_verified', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        return self.create_user(first_name, last_name, contact_number, password, **other_fields)

    def create_user(self, first_name, last_name, contact_number, password, **other_fields):
        if not first_name:
            raise ValueError('Users must provide a first name.')
        if not last_name:
            raise ValueError('Users must provide a last name.')
        if not contact_number:
            raise ValueError('Users must provide a contact number.')
        # email = self.normalize_email(email)
        user = self.model(first_name=first_name,
                          last_name=last_name, contact_number=contact_number, **other_fields)
        user.set_password(password)
        user.save()


class User(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = PhoneNumberField(blank=False, null=False, unique=True)
    show_contact_number = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, blank=True)
    is_contact_number_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False) #represents if the account of the user is blocked by admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) #represents if the account of the user is active or inactive due to different reasons
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(default='default_profile.jpg', upload_to='profile_pics', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    no_sold_items = models.IntegerField(null=False, default=0, blank=True) #represents the total number of items sold by the user

    objects = AccountManager()

    USERNAME_FIELD = 'contact_number'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_pic:
            if storage.exists(self.profile_pic.name):
                img_read = storage.open(self.profile_pic.name, "r")
                img = Image.open(img_read)
                img_buffer = BytesIO()
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size, Image.ANTIALIAS)
                    img.save(img_buffer, img.format)
                    img.show()
                    self.profile_pic.save(self.profile_pic.name, ContentFile(img_buffer.getvalue()))
                img_read.close()

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser
# ....................CUSTOM USER MODEL...........................


class Thread(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')


class Message(models.Model):
	thread = models.ForeignKey(Thread, related_name='message', on_delete=models.CASCADE, blank=True, null=True)
	body = models.CharField(max_length=1000)
	date = models.DateTimeField(default=timezone.now)