from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    email = models.EmailField(db_index=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_first_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        first_name = "%s " % (self.first_name)
        return first_name.strip()




class App_models(models.Model):
    app_name=models.TextField(max_length=200)
    app_code=models.TextField(max_length=100)

    def __str__(self):
        return self.app_name


    def appcode(self):
        return self.app_code

class SWorker(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    app_name =models.ForeignKey(App_models,on_delete=models.CASCADE)
    work_name=models.CharField(max_length=100)
    work_descp =models.TextField(max_length=700)
    work_time =models.DateField(default=None)
    time=models.TextField(max_length=200)
    work_status=models.BooleanField(default=False)
    permission_status = models.BooleanField(default=False)



    def __str__(self):
        return self.name

class work_type(models.Model):
    app_name=models.ForeignKey(App_models,on_delete=models.CASCADE)
    description=models.TextField(max_length=100)

    # def __str__(self):
    #     return self.app_name
class worker_role(models.Model):
    is_Lmanager=models.BooleanField(default=False)
    role_id=models.ForeignKey(User,on_delete=models.CASCADE)