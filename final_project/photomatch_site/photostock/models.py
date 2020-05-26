import hashlib

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

def get_image_name(instance, filename):
    h = hashlib.md5(str(instance).encode()).hexdigest()
    frmt = filename.split('.')[-1].lower()
    return f'user_avatars/{h}_avatar.{frmt}' #

class Profile(models.Model):
    LIST_OF_ALL_GENDERS = [
        ('ns', 'Not specified'),
        ('m', 'Male'),
        ('f', 'Female'),
        ('nb', 'Non-binary'),        
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=2, choices=LIST_OF_ALL_GENDERS, default='ns')
    # avatar = models.ImageField(upload_to=get_image_name)
    #
    # def save(self, *args, **kwargs):        
    #     try:
    #         this = Human.objects.get(id=self.id)
    #         if this.avatar != self.avatar:
    #             this.avatar.delete(save=False)
    #     except: pass
    #     super(Human, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.username}: {self.user.first_name} {self.user.last_name}'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
