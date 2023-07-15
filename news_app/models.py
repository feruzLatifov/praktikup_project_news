from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
# from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class PulishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.Published)

class Category(models.Model):
     name = models.CharField(max_length=150)
     def __str__(self):
          return self.name

class News(models.Model):

     class Status(models.TextChoices):
          Draft = "DF", "Draft"
          Published = "PB", "Published"

     title = models.CharField(max_length=250)
     slug = models.SlugField(max_length=250, blank=True, null=True)
     body = RichTextUploadingField()
     image = models.ImageField(upload_to='news/images')
     category = models.ForeignKey(Category,
                                  on_delete=models.CASCADE
                                  )
     publish_time = models.DateTimeField(default=timezone.now)
     created_time = models.DateTimeField(auto_now_add=True)
     update_time = models.DateTimeField(auto_now=True)
     status = models.CharField(max_length=2,
                               choices=Status.choices,
                               default=Status.Draft
                               )
     # view_count = models.IntegerField(default=0) #1-usul bu ko'rilganlarni sonini aniqlash
     objects = models.Manager() # default manager
     published = PulishedManager()

     class Meta:
          ordering = ["-publish_time"]

     def __str__(self):
          return self.title

     # def save(self, *args, **kwargs):
     #     self.slug = slugify(self.title)
     #     super().save(*args, **kwargs)

     def get_absolute_url(self):
         return reverse("news_detail_page", args=[self.slug])

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.email

class Comment(models.Model):
    news = models.ForeignKey(News,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments')
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return f"Comment = {self.body} by {self.user}"