from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import MemberManager
import uuid
from django.db.models.deletion import CASCADE
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Member(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MemberManager()

    def __str__(self):
        return self.email

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Member, on_delete=CASCADE, related_name="editorals")
    published_date = models.DateTimeField(auto_now_add=True, editable=False)
    snippet = models.CharField(max_length=250)
    text = RichTextField()
    slug = models.SlugField(unique=True, db_index=True, blank=True, max_length=255)
    tags = models.ManyToManyField(Tag)
    image = models.URLField()
    top_post = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Member, on_delete=CASCADE, related_name="threads")
    published_date = models.DateTimeField(auto_now_add=True, editable=False)
    text = RichTextField()
    slug = models.SlugField(unique=True, db_index=True, blank=True, max_length=255)
    tags = models.ManyToManyField(Tag)
    image = models.URLField()
    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Thread, self).save(*args, **kwargs)

class Comment(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(Thread,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80) 
    email = models.ForeignKey(
        Member, on_delete=CASCADE, related_name="user_comments")
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 

    class Meta: 
        ordering = ('created',) 

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post)