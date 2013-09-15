from django.db import models
import datetime
import os

VISIBILITY_PUBLIC = 1
VISIBILITY_PRIVATE = 2
VISIBILITY_UNLISTED = 3

VISIBILITY_CHOICES = (
    (VISIBILITY_PUBLIC, 'Public'),
    (VISIBILITY_PRIVATE, 'Private'),
    (VISIBILITY_UNLISTED, 'Unlisted'),
)

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __unicode__(self):
        return self.name


def get_upload_path(instance, filename):
    return os.path.join(
        "%d" % instance.publish_date.year,
        "%d" %  instance.publish_date.month,
        "%s.png" % instance.slug
    )

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    teaser_image = models.ImageField(upload_to=get_upload_path)
    teaser = models.TextField(max_length=500)
    content = models.TextField(max_length=10000)
    slug = models.SlugField()
    category = models.ForeignKey(Category)
    tag = models.ManyToManyField(Tag)
    publish_date = models.DateTimeField(default=datetime.datetime.now())
    visibility = models.SmallIntegerField(default=VISIBILITY_PUBLIC, choices=VISIBILITY_CHOICES)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-publish_date']

    def __unicode__(self):
        return self.title
