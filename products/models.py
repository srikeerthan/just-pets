from django.db import models
from django.db.models.signals import pre_save

from core.helper import file_size, unique_slug_generator
from ckeditor.fields import RichTextField


# Create your models here.

class Product(models.Model):
    # Basic Information
    title = models.CharField(max_length=500)
    brand = models.CharField(max_length=120, blank=True)

    # pricing
    selling_price = models.BigIntegerField()
    offering_price = models.BigIntegerField()

    image = models.ImageField(upload_to='product/', validators=[file_size])

    description = RichTextField(blank=True)

    slug = models.SlugField(null=True, unique=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("-updated_at",)


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance=instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
