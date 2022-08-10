from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Item, SoldStatus


@receiver(post_save, sender=Item)
def create_sold_status(sender, instance, created, **kwargs):
    if created:
        """Create a SoldStatus object for every Item object created."""
        SoldStatus.objects.create(item=instance, sold_price=0)

        """Update the item with a slug as soon as the item object is created."""
        instance.slug = slugify(instance.name) + '-' + str(instance.id)
        instance.save()


@receiver(post_save, sender=Item)
def save_item(sender, instance, **kwargs):
    instance.sold_status.save()
