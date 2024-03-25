from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

    
class MembersManager(BaseUserManager):
    def create_user(self, name, email, phone_number, verification_code, password, **extra_fields):
        email = email.lower()
        user = self.model(name=name, email=email, phone_number=phone_number, verification_code=verification_code, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        
        return user


class Members(AbstractBaseUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique = True)
    phone_number = models.CharField(max_length=15)
    is_varified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6)
    is_member = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = MembersManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
