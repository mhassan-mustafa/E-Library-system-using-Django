from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
import os


class AdminsManager(BaseUserManager):
    def create_user(self, name, username, password, **extra_fields):
        user = self.model(name=name, username=username, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        
        return user


class Admins(AbstractBaseUser):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique = True)
    is_admin = models.BooleanField(default=True)
    is_member = models.BooleanField(default=False)
    
    objects = AdminsManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Books(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    isbn = models.IntegerField()
    rating = models.IntegerField()
    pages = models.IntegerField()
    image = models.ImageField(upload_to="images/", default="default.png")
    pdf = models.FileField(upload_to="pdfs/", default="default.pdf")


@receiver(pre_delete, sender=Books)
def delete_image(sender, instance, **kwargs):
    # Delete the associated image file when the record deleted from database.
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            
    # Delete the associated pdf file when the record deleted from database.
    if instance.pdf:
        if os.path.isfile(instance.pdf.path):
            os.remove(instance.pdf.path)
            
            
@receiver(pre_save, sender=Books)
def pre_save_image(sender, instance, **kwargs):
    
    if instance.pk:
        try:
             
            old_instance = sender.objects.get(pk=instance.pk)
            # when we edit Book record, old image will replaced with new one.
            if old_instance.image != instance.image:
                if os.path.isfile(old_instance.image.path):
                    os.remove(old_instance.image.path)
            elif old_instance.image:
                if os.path.isfile(old_instance.image.path):
                    os.remove(old_instance.image.path)

            # when we edit Book record, old pdf will replaced with new one.
            if old_instance.pdf != instance.pdf:
                if os.path.isfile(old_instance.pdf.path):
                    os.remove(old_instance.pdf.path)
            elif old_instance.pdf:
                if os.path.isfile(old_instance.pdf.path):
                    os.remove(old_instance.pdf.path)
    
        except sender.DoesNotExist:
            pass