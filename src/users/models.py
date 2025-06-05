from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUserManager(UserManager):
    def _create_user(self, username, password, **extras):
        if not username:
            raise ValueError('Invalid Username')
        if not extras['email']:
            raise ValueError('Invalid Email')
        if not password:
            raise ValueError('Invalid Password')
        
        email = self.normalize_email(extras['email'])

        user = self.model(username=username, **extras)
        user.set_password(password)
        user.save()

        return user
    
    def create_user(self, username, password, **extras):
        extras.setdefault('is_staff', False)
        extras.setdefault('is_superuser', False)
        extras.setdefault('is_active', True)

        return self._create_user(username, password, **extras)

    def create_superuser(self, username, password, **extras):
        extras.setdefault('is_staff', True)
        extras.setdefault('is_superuser', True)
        extras.setdefault('is_active', True)

        return self._create_user(username, password, **extras)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, unique=True, null=False, blank=False)
    email = models.CharField(max_length=255, unique=True, null=False, blank=False)
    level = models.IntegerField(null=False, blank=False, default=1, validators=[MaxValueValidator(6)])
    peaced_gardens = models.IntegerField(null=False, blank=False, default=0)
    last_garden = models.ForeignKey('gardens.Garden', on_delete=models.SET_NULL, default=None, null=True)
    xp_amount = models.IntegerField(null=False, blank=False, default=0, validators=[MaxValueValidator(600)])
    is_staff = models.BooleanField(default=False, null=False, blank=False)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    date_joined = models.DateTimeField(default=timezone.now, null=False, blank=False)
    last_login = models.DateTimeField(default=None, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def gain_xp(self, garden_level):
        bonus_xp_gained = (garden_level - self.level) * 25
        if bonus_xp_gained < 0:
            bonus_xp_gained = 0
        xp_gained = bonus_xp_gained + 20
        self.xp_amount += xp_gained
        while self.xp_amount > self.level * 100:
            self.xp_amount -= self.level * 100
            self.level += 1
        self.save()
        




