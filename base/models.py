from django.db import models
from taggit.managers import TaggableManager


class Listing(models.Model):
    title = models.CharField(max_length=255)
    tags = TaggableManager(blank=True)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True)
    website = models.CharField(max_length=255)
    logo = models.ImageField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title