from django.db import models
from store.models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #type (product,video,article)
    # ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
