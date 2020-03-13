from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length = 250)
    username = models.CharField(max_length = 250, unique = True)
    email = models.CharField(max_length = 250, unique = True)
    phone = models.PositiveIntegerField()
    gender = models.CharField(max_length = 250)
    address = models.CharField(max_length = 1000)
    business = models.CharField(max_length = 250)
    bio = models.CharField(max_length = 2000)
    password = models.CharField(max_length = 250)
    pic = models.ImageField(upload_to = 'images/', null = True, verbose_name = "")
    BAN = models.CharField(max_length = 250)
    chat = models.CharField(max_length = 1024)    

    def __str__(self):
        return self.username
    
class Image(models.Model):
    username = models.CharField(max_length = 250)
    email = models.CharField(max_length = 250)
    image_file = models.ImageField(upload_to = 'images/', null = True, verbose_name = "")
    auto = models.AutoField(primary_key = True)
    comments = models.CharField(max_length = 1024)

    BAN = models.CharField(max_length = 250)
    
    def __str__(self):
        return self.email + " : " + str(self.image_file)
    
class Chat(models.Model):
    auto = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 250)
    chat = models.CharField(max_length = 1024)
     

    def __str__(self):
        return str(self.auto) + " : " + self.username

class Box(models.Model):
    sender = models.CharField(max_length = 250)
    receiver = models.CharField(max_length = 250)
    chat = models.CharField(max_length = 1024)
    auto = models.AutoField(primary_key = True)
    notification = models.PositiveIntegerField()

    def __str__(self):
        return self.sender + " : " + self.receiver
