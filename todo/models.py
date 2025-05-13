import re

from django.core.files.storage import default_storage
from django.db import models

# Create your models here.

# models.py

from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
from pathlib import Path
from io import BytesIO

User = get_user_model()


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    thumbnail = models.ImageField(
        upload_to='thumbnails/', null=True, blank=True
    )
    completed_image = models.ImageField(upload_to='completed_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_preview_image_url(self):
        if self.thumbnail and self.thumbnail.name:
            return self.thumbnail.url
        if self.completed_image and self.completed_image.name:
            return self.completed_image.url
        match = re.search(r'<img[^>]+src=[\'"](?P<src>[^\'"]+)[\'"]', self.description or "", re.IGNORECASE)
        if match:
            return match.group("src")
        return None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.completed_image:
            return super().save(*args, **kwargs)

        image = Image.open(self.completed_image)
        image.thumbnail((100, 100))

        image_path = Path(self.completed_image.name)

        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix
        thumbnail_filename = f'{thumbnail_name}_thumbnail{thumbnail_extension}'

        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, format=file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)

        temp_thumb.close()
        return super().save(*args, **kwargs)

class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}: {self.message}'