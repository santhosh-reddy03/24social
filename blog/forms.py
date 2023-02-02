from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post", "date"]
        labels = {
            "user_email": "your email",
            "user_name": "Your name",
            "text": "Your Comment",
        }
        error_messages = {"required": "Cannot submit empty comment"}
