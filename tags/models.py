from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# This models are to implement generic relationships that can be reused in
# any project, we want the ability to tag items.

# Tag class represent an actual tag
class Tag(models.Model):
    label = models.CharField(max_length=255)


# TaggedItem represents a tag applied to a particular item
# by using this class we can find what tag is applied to what object
class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # To keep the two apps separated we need a generic way to identify an object
    # We use two pieces of info Type(product, video, article, etc) and ID.
    # using the type we can find the table and using Id we can find the record
    # we use an Abstract model called Content Type, that comes with Django that allows
    # the creation of generic relations
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # we might want to get the actual object this tag is applied to, we use a GenericForeignKey
    content_object = GenericForeignKey()
