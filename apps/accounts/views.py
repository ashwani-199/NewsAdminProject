from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.contrib import messages
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import User, EmailVerification, PasswordReset
from apps.accounts.forms import UserRegistrationForm, UserLoginForm, UserProfileForm, UserPasswordChangeForm, ForgotPasswordForm


class RegisterView(View):
    template_name = 'account/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('news:home')
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            token = get_random_string(64)
            EmailVerification.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timezone.timedelta(hours=24)
            )
            verification_url = request.build_absolute_uri(
                reverse('account:verify_email', args=[token])
            )
            subject = 'Verify your email address'
            message = render_to_string('emails/verify_email.html', {
                'user': user,
                'verification_url': verification_url,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.success(request, 'Account created! Check your email to verify your account.')
            return redirect('account:login')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'account/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('news:home')
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_email_verified:
                    messages.warning(request, 'Please verify your email address first.')
                    return redirect('account:login')
                login(request, user)
                user.last_active = timezone.now()
                user.save(update_fields=['last_active'])
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                next_url = request.GET.get('next')
                return redirect(next_url or 'news:home')
        return render(request, self.template_name, {'form': form})


class LogoutView(AuthLogoutView):
    next_page = 'news:home'


class VerifyEmailView(View):
    def get(self, request, token):
        verification = get_object_or_404(EmailVerification, token=token, is_used=False)
        if verification.expires_at < timezone.now():
            messages.error(request, 'Verification link has expired.')
            return redirect('account:login')
        user = verification.user
        user.is_email_verified = True
        user.email_verified_at = timezone.now()
        user.is_active = True
        user.save(update_fields=['is_email_verified', 'email_verified_at', 'is_active'])
        verification.is_used = True
        verification.save(update_fields=['is_used'])
        messages.success(request, 'Email verified! You can now log in.')
        return redirect('account:login')


class ForgotPasswordView(View):
    template_name = 'account/forgot_password.html'

    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            token = get_random_string(64)
            PasswordReset.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timezone.timedelta(hours=1)
            )
            reset_url = request.build_absolute_uri(
                reverse('account:reset_password', args=[token])
            )
            subject = 'Reset your password'
            message = render_to_string('emails/password_reset.html', {
                'user': user,
                'reset_url': reset_url,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            messages.success(request, 'Check your email for password reset instructions.')
            return redirect('account:login')
        return render(request, self.template_name, {'form': form})


class ResetPasswordView(View):
    template_name = 'account/reset_password.html'

    def get(self, request, token):
        reset = get_object_or_404(PasswordReset, token=token, is_used=False)
        if reset.expires_at < timezone.now():
            messages.error(request, 'Reset link has expired.')
            return redirect('account:forgot_password')
        return render(request, self.template_name, {'token': token})

    def post(self, request, token):
        reset = get_object_or_404(PasswordReset, token=token, is_used=False)
        if reset.expires_at < timezone.now():
            messages.error(request, 'Reset link has expired.')
            return redirect('account:forgot_password')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, self.template_name, {'token': token})
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, self.template_name, {'token': token})
        user = reset.user
        user.set_password(password)
        user.save(update_fields=['password'])
        reset.is_used = True
        reset.save(update_fields=['is_used'])
        messages.success(request, 'Password reset successful! You can now log in.')
        return redirect('account:login')
