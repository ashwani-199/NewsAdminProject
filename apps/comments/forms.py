from django import forms
from apps.comments.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg resize-none',
                'rows': 4,
                'placeholder': 'Write your comment...',
            }),
        }
        labels = {
            'content': '',
        }
