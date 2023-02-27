from django import forms

from .models import Comment


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
