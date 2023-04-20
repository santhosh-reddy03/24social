from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Tags(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.caption}"


class Post(models.Model):
    image = models.ImageField(upload_to="images", blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    date = models.DateField()
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    content = models.TextField()
    tags = models.ManyToManyField(Tags)
    slug = models.SlugField(unique=True, db_index=True)
    total_likes = models.BigIntegerField()

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("detailed_post", args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user_name = models.CharField(max_length=30)
    user_email = models.EmailField()
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.text} posted on {self.date}"
