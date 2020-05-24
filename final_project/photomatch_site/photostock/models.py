from django.db import models
from PIL import Image

def get_image_name(instance, filename):
    print(filename)    
    frmt = filename.split('.')[-1]
    return f'user_avatars/user{instance.id}_avatar.{frmt}'

class Human(models.Model):
    LIST_OF_ALL_GENDERS = [
        ('ns', 'Not specified'),
        ('m', 'Male'),
        ('f', 'Female'),
        ('nb', 'Non-binary'),        
    ]
    avatar = models.ImageField(upload_to=get_image_name)
    first_name = models.CharField(max_length=256)
    second_name = models.CharField(max_length=256)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=2, choices=LIST_OF_ALL_GENDERS, default='ns')

    def save(self):
        if self.avatar:
            super(Human, self).save()
            image = Image.open(self.avatar)
            image.thumbnail((250,150), Image.ANTIALIAS)
            image.save(self.avatar.path+'thumbnail_200_200_aa.jpg', 'JPEG', quality=75)

    def __str__(self):
       return f'{self.first_name} {self.second_name}'