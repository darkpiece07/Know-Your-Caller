from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('The Email or Phone Number field must be set')
        email = self.normalize_email(email) if email else None
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length = 15, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Add is_staff field
    is_superuser = models.BooleanField(default=False)  # Add is_superuser field

    
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'  # Use 'phone_number' as the unique identifier for authentication
    REQUIRED_FIELDS = ['email', 'name']  # Additional fields required when using createsuperuser command

    
    groups = models.ManyToManyField(Group, related_name='user_set_knowyourcallerapp', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set_knowyourcallerapp',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


    def __str__(self):
        return self.phone_number


#global database for all phone numbers ,  a phone number can have different names
#because mulitiple users will save same particular number with differet names
#one slight loophole is that number, spamlikelihood will be same and names will be different and this
#table will have more data for the same number.. further improvement can be done

# Phone_Book or Contact_list of all users are stored via this model 
class PhoneNumber(models.Model):
    name = models.CharField(max_length=255, default = "unknown")
    number = models.CharField(max_length=15)
    spam_likelihood = models.IntegerField(default=0)

    def __str__(self):
        return self.number
    
    

class SpamAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)
    is_marked_as_spam = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name
    
#contact_name = name & contact_number = phone_number
class UserContact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"