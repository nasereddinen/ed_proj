from distutils.command.upload import upload
from email.mime import image
from pyexpat import model
from tkinter import CASCADE
from turtle import title
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    biographie = models.TextField(max_length=280)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    specialite = models.CharField(max_length=20,null=False, blank=True)
    experience = models.CharField(max_length=20,null=False, blank=True)
    City =  models.CharField(max_length=20,null=False, blank=True)
    Parcour =  models.CharField(max_length=20,null=False, blank=True)
    linkedin = models.CharField(max_length=20,null=False)
    skills = models.CharField(max_length=280)
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.username
        
class Category(models.Model):
    title = models.CharField(max_length=100)
    top_ten_cat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')
    def __str__(self):
        return self.title

class language(models.Model):
    langue = models.CharField(max_length=200)
    def __str__(self):
        return self.langue

class subcat(models.Model):
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcat', blank = True, null=True, help_text='Select Only Sub Category')
    title = models.CharField(max_length=100) 
    created_at = models.DateTimeField(auto_now_add=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')

    def __str__(self):
        return self.title

#############################sujet######################
class Sujet(models.Model):
    title = models.CharField(max_length=70)
    reqs = models.CharField(max_length=2000, verbose_name='description',blank=True)
    author = models.CharField(max_length=100,blank=True)
    images = models.ImageField(upload_to='media/image_sujet',blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    follows= models.ManyToManyField(User,related_name="sujet_follows",blank=True)
    def __str__(self):
        return self.title
    def count_follow(self):
        return self.follows.all().count()

class blog(models.Model):
    title = models.CharField(max_length=70)
    meta_tags = models.CharField(max_length=2000, blank=True)
    meta_desc = models.TextField(max_length=2000, blank=True)
    image = models.ImageField(upload_to='media/imageblog')
    image_alt_name = models.CharField(max_length=200, blank=True)
    desc = RichTextField(blank=True, null=True)
    likes= models.ManyToManyField(User,related_name='blog_likes',blank=True)
    author = models.CharField(max_length=20, default="admin" )
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Sujet, on_delete=models.CASCADE,related_name="blog")
    hit = models.PositiveIntegerField(default=0)
    disc = models.BooleanField(default=False, verbose_name='discription')  
    def __str__(self):
        return self.title    

class BlogComment(models.Model):
    blog=models.ForeignKey(blog,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} comment"
###########cours   
class cours(models.Model):
    title = models.CharField(max_length=70)
    reqs = models.CharField(max_length=2000, blank=True,)
    likes = models.ManyToManyField(User,related_name="cour_likes",blank=True)
    image = models.ImageField(upload_to='media/image_cours')
    image_alt_name = models.CharField(max_length=200, blank=True)
    desciption = models.TextField(blank=True, null=True)
    teacher = models.CharField(max_length=20, default="admin" )
    date = models.DateTimeField(auto_now_add=True)
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE)
    like = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    langue = models.ForeignKey(language,on_delete=models.CASCADE)
    def num_likes(self):
        return self.likes.count()
    #annonce
class annonce(models.Model):
    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=2000, blank=True)
    desc = models.TextField(max_length=200, blank=True)
    author = models.CharField(max_length=20, default="student")

    def __str__(self):
        return self.title

    def count_like(self):
        self.likes.count()

#folder function
def cour_directory_path(instance,filename):
    return "video_files/cours_{0}/{1}".format(instance.cour.id, filename)
#--videos
class VideoCours(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video=models.FileField(upload_to=cour_directory_path)
    uploaded=models.DateTimeField(auto_now_add=True)
    cour = models.ForeignKey(cours,on_delete=models.CASCADE)
    titre= models.CharField(max_length=200,blank=True)
    chapitre = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.titre
    def delete(self,*args,**kwargs):
        self.video.delete()
        super().delete(*args,**kwargs)
    
class Order(models.Model):
    course = models.ForeignKey(cours,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    ordred = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
#question
class question(models.Model):
    sujet = models.ForeignKey(Sujet,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.TextField(max_length=200, blank=True)
    author = models.CharField(max_length=20, default="guest" )
    def __str__(self):
        return self.title

class notes(models.Model):
    chapitre = models.ForeignKey(VideoCours,on_delete=models.CASCADE)
    text_note = RichTextField(config_name ='notes',blank=True, null=True)
    student = models.ForeignKey(User,models.CASCADE)