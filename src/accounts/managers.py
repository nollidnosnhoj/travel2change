from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    # Creates Active User
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError(_('Email Address is required'))
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    # Creates Super User
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff = True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True'))
        return self.create_user(email, first_name, last_name, password, **extra_fields)

    # Create Staff User
    def create_staffuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Staffuser must have is_staff = True'))
        return self.create_user(email, first_name, last_name, password, **extra_fields)
