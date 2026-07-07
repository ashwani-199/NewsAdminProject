from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from apps.accounts.forms import UserProfileForm, UserPasswordChangeForm
from apps.news.models import Bookmark, ArticleView
from apps.comments.models import Comment
from apps.notifications.models import Notification


class UserDashboardView(LoginRequiredMixin, View):
    template_name = 'users/dashboard.html'

    def get(self, request):
        context = {
            'total_bookmarks': Bookmark.objects.filter(user=request.user).count(),
            'total_comments': Comment.objects.filter(user=request.user).count(),
            'total_views': ArticleView.objects.filter(user=request.user).count(),
            'unread_notifications': Notification.objects.filter(
                recipient=request.user, is_read=False
            ).count(),
            'recent_bookmarks': Bookmark.objects.filter(user=request.user)[:5],
        }
        return render(request, self.template_name, context)


class EditProfileView(LoginRequiredMixin, View):
    template_name = 'users/edit_profile.html'

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:edit_profile')
        return render(request, self.template_name, {'form': form})


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'users/change_password.html'

    def get(self, request):
        form = UserPasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('users:change_password')
        return render(request, self.template_name, {'form': form})


class BookmarksView(LoginRequiredMixin, View):
    template_name = 'users/bookmarks.html'

    def get(self, request):
        bookmarks = Bookmark.objects.filter(user=request.user).select_related('article__author', 'article__category')
        return render(request, self.template_name, {'bookmarks': bookmarks})


class ReadingHistoryView(LoginRequiredMixin, View):
    template_name = 'users/reading_history.html'

    def get(self, request):
        history = ArticleView.objects.filter(user=request.user).select_related('article')[:100]
        return render(request, self.template_name, {'history': history})


class MyCommentsView(LoginRequiredMixin, View):
    template_name = 'users/my_comments.html'

    def get(self, request):
        comments = Comment.objects.filter(user=request.user).select_related('article')[:50]
        return render(request, self.template_name, {'comments': comments})


class UserNotificationsView(LoginRequiredMixin, View):
    template_name = 'users/notifications.html'

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user)[:50]
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return render(request, self.template_name, {'notifications': notifications})


class NewsletterSettingsView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        user.receive_newsletter = request.POST.get('receive_newsletter') == 'on'
        user.save(update_fields=['receive_newsletter'])
        messages.success(request, 'Newsletter preferences updated!')
        return redirect('users:dashboard')
