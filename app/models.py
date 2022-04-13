from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.db.models.deletion import CASCADE
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Member(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

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

    class Meta:
        ordering = ['-published_date']

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
    tags = models.ManyToManyField(Tag, blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Thread, self).save(*args, **kwargs)
    
    @property
    def latest_comment_date(self):
        latest_comment = self.published_date
        comments = self.comments.all()
        if len(comments) > 0:
            latest_comment = comments[0].created
        return latest_comment

    @property
    def num_of_comments(self):
        number_of_comments = 0
        comments = self.comments.all()
        if len(comments) > 0:
            number_of_comments = len(comments)
        return number_of_comments




class Comment(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(Thread,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(
        Member, on_delete=CASCADE, related_name="user_comments")
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 

    class Meta: 
        ordering = ('-created',) 

    def __str__(self): 
        return f"Comment by {self.user} on Thread {self.thread}"