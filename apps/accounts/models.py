from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    USER_ROLES = (
        ('guest', 'Guest'),
        ('registered', 'Registered User'),
        ('journalist', 'Journalist/Author'),
        ('editor', 'Editor'),
        ('administrator', 'Administrator'),
    )

    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='registered')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    receive_newsletter = models.BooleanField(default=True)
    last_active = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_journalist(self):
        return self.role == 'journalist'

    @property
    def is_editor(self):
        return self.role == 'editor' or self.is_staff

    @property
    def can_publish(self):
        return self.role in ['journalist', 'editor', 'administrator'] or self.is_staff


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Email Verification')
        verbose_name_plural = _('Email Verifications')

    def __str__(self):
        return f'{self.user.email} - {self.token[:20]}...'


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_resets')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Password Reset')
        verbose_name_plural = _('Password Resets')

    def __str__(self):
        return f'{self.user.email} - {self.token[:20]}...'


class AuthorIDCard(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='id_cards')
    card_id = models.CharField(max_length=30, unique=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_cards')
    rejection_reason = models.TextField(blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Author ID Card')
        verbose_name_plural = _('Author ID Cards')
        ordering = ['-requested_at']

    def __str__(self):
        return f'{self.card_id} - {self.user.get_full_name() or self.user.username}'

    def save(self, *args, **kwargs):
        if not self.card_id:
            last = AuthorIDCard.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.card_id = f'NP-JOURNALIST-{num:04d}'
        super().save(*args, **kwargs)
