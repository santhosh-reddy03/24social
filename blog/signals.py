from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
import os
from blog.models import Post
from django.db import transaction


@receiver(post_delete, sender=Post)
def auto_delete_images_on_delete(sender, instance, **kwargs):
    """deletes if the deleted post has any images"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Post)
def auto_delete_files_on_change(sender, instance, **kwargs):
    """
    deletes the old file if the file is updated
    """
    if not instance.pk:
        return False
    try:
        old_image_file = Post.objects.get(pk=instance.pk).image
    except Post.DoesNotExist:
        return False
    new_image_file = instance.image
    if not new_image_file == old_image_file:
        if os.path.isfile(old_image_file.path):
            transaction.on_commit(lambda: os.remove(old_image_file.path))
