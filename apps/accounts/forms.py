from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500', 'placeholder': 'you@example.com'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500', 'placeholder': 'Choose a username'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500 pr-10', 'placeholder': 'Create a password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500 pr-10', 'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('A user with this email already exists.'))
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500', 'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500', 'placeholder': 'Password'})
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'phone', 'location', 'website', 'avatar',
                  'twitter_handle', 'facebook_url', 'linkedin_url']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'bio': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'rows': 4}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'website': forms.URLInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'twitter_handle': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'facebook_url': forms.URLInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'})
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'placeholder': 'Enter your email'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('No user found with this email address.'))
        return email
