from django.db import models
from django.contrib.auth.models import User
import os

def path_and_rename(instance, filename):
    upload_to = 'static/img/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.name:
        print('--------------------------------------------------------------------------')
        print(instance.name)
        filename = '{}.{}'.format(instance.name, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format('Unkown', ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Case(models.Model):
    name=models.CharField(max_length=256)
    age=models.CharField(max_length=256)
    gender=models.CharField(max_length=256)
    #email= models.EmailField(max_length=254)
    #phone = PhoneNumberField(null=False, blank=False, unique=True)
    image=models.ImageField(null=False,blank=False,upload_to=path_and_rename)
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    #FileTime=models.DateTimeField(verbose_name='Case File At Time',auto_now_add=True)
    #found=models.BooleanField(verbose_name='Person Found Or Not',default=False)
    # Additional Attributes

#class Details(models.Model):
    #add=models.ForeignKey(Photo,on_delete=models.CASCADE)
    #name=models.CharField(max_length=256)
    #age=models.CharField(max_length=256)
    #gender=models.CharField(max_length=256)
    #image=models.ImageField(null=False,blank=False)

    #def __str__(self):
        #return self.name
# class ImageAlbum(models.Model):
#     def default(self):
#         return self.images.filter(default=True).first()
# class Image(models.Model):
#     name = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='static/img')
#     default = models.BooleanField(default=False)
#     width = models.FloatField(default=100)
#     length = models.FloatField(default=100)
#     album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE)

class CaseImages(models.Model):
    image=models.ImageField(null=False,blank=False,upload_to='static/img')
    case=models.ForeignKey(to=Case,on_delete=models.CASCADE)
