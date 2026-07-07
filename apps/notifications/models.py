from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('new_comment', 'New Comment'),
        ('new_reply', 'New Reply'),
        ('breaking_news', 'Breaking News'),
        ('newsletter', 'Newsletter'),
        ('admin_message', 'Admin Message'),
        ('article_published', 'Article Published'),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['recipient', '-created_at']),
        ]

    def __str__(self):
        return f'{self.recipient.username} - {self.title[:50]}'


class NotificationPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    new_comment = models.BooleanField(default=True)
    new_reply = models.BooleanField(default=True)
    breaking_news = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=True)
    admin_message = models.BooleanField(default=True)
    article_published = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} preferences'
