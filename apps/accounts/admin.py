from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User, EmailVerification, PasswordReset, AuthorIDCard


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_email_verified', 'is_active', 'date_joined']
    list_filter = ['role', 'is_email_verified', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'location', 'bio')}),
        (_('Profile'), {'fields': ('avatar', 'website', 'twitter_handle', 'facebook_url', 'linkedin_url')}),
        (_('Permissions'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Email'), {'fields': ('is_email_verified', 'email_verified_at', 'receive_newsletter')}),
        (_('Important dates'), {'fields': ('last_login', 'last_active', 'date_joined')}),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']


@admin.register(AuthorIDCard)
class AuthorIDCardAdmin(admin.ModelAdmin):
    list_display = ['card_id', 'user', 'status', 'requested_at', 'approved_at', 'approved_by', 'is_active']
    list_filter = ['status', 'is_active', 'requested_at']
    search_fields = ['card_id', 'user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['card_id', 'requested_at', 'approved_at', 'approved_by']

    def approve_id_card(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='approved', approved_at=timezone.now(), approved_by=request.user)
    approve_id_card.short_description = 'Approve selected ID cards'

    def reject_id_card(self, request, queryset):
        queryset.update(status='rejected')
    reject_id_card.short_description = 'Reject selected ID cards'

    actions = [approve_id_card, reject_id_card]
