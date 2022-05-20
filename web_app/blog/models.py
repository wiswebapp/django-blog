from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    status = models.IntegerField(default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    status = models.IntegerField(default='1')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('Tags')


class Blog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField()
    # blog_img = models.ImageField(upload_to="blog/images", default='untitled.png')
    tags = models.ManyToManyField(Tag)
    is_published = models.IntegerField(default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.title:
            self.title = self.title.strip()
        if self.description:
            self.description = self.description.strip()
            
    @property
    def blog_with_cat(self):
        return self.title

class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=250, default=None)
    path = models.ImageField(upload_to="blog/images", default='blog/no-blog-found.jpg')
    status = models.IntegerField(default='1')

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=250, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Contact Form Filled by ' + self.name + "("  + self.email + ")"
"""
    Reference : https://docs.djangoproject.com/en/4.0/ref/models/fields/
"""
