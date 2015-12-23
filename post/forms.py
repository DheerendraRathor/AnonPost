from django import forms
from models import Post, Reply
from redactor.widgets import RedactorEditor


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'message']
        widgets = {
            'message': RedactorEditor(attrs={'id': 'detail', 'placeholder': 'Enter details'}, allow_image_upload=False)
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['message']
        widgets = {
            'message': RedactorEditor(
                attrs={
                    'id': 'reply-textarea',
                    'placeholder': 'Add Reply',
                    'row': '3',
                },
                allow_image_upload=False,
            )
        }
