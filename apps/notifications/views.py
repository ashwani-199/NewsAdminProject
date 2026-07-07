from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from apps.notifications.models import Notification


class NotificationListView(LoginRequiredMixin, View):
    template_name = 'notifications/list.html'

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user)[:50]
        return render(request, self.template_name, {'notifications': notifications})


class MarkNotificationRead(LoginRequiredMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return redirect(notification.link or 'notifications:notifications')


class MarkAllRead(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return redirect('notifications:notifications')


class UnreadCountView(LoginRequiredMixin, View):
    def get(self, request):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return JsonResponse({'count': count})
