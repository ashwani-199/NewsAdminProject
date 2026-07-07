from django.db import models
from django.core.validators import FileExtensionValidator


class Advertisement(models.Model):
    POSITION_CHOICES = (
        ('header', 'Header'),
        ('sidebar', 'Sidebar'),
        ('footer', 'Footer'),
        ('in_article', 'In-Article'),
        ('popup', 'Popup'),
        ('banner', 'Banner'),
    )

    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='ads/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])]
    )
    script_code = models.TextField(blank=True, help_text='Ad script code (e.g., Google AdSense)')
    url = models.URLField(blank=True, help_text='Link URL for image ad')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    clicks_count = models.PositiveIntegerField(default=0, editable=False)
    impressions_count = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position', 'order']

    def __str__(self):
        return f'{self.get_position_display()} - {self.title}'

    @property
    def is_valid(self):
        now = timezone.now()
        if self.start_date and self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True
