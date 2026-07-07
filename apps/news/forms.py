from django import forms
from apps.news.models import Article, Category
from taggit.forms import TagWidget


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'content', 'category', 'tags', 'featured_image',
                  'featured_image_alt', 'status', 'is_featured', 'is_breaking', 'is_trending',
                  'is_editor_pick', 'allow_comments', 'scheduled_at',
                  'meta_title', 'meta_description', 'meta_keywords']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'placeholder': 'Article title'}),
            'summary': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'rows': 3, 'placeholder': 'Brief summary'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'tags': TagWidget(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'placeholder': 'tag1, tag2, tag3'}),
            'featured_image_alt': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'status': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'scheduled_at': forms.DateTimeInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'type': 'datetime-local'}),
            'meta_title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'placeholder': 'SEO title (max 70 chars)'}),
            'meta_description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'rows': 2, 'placeholder': 'SEO description (max 160 chars)'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'placeholder': 'keyword1, keyword2, keyword3'}),
        }
