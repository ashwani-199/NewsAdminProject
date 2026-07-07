from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from apps.newsletter.models import Subscriber


class SubscribeView(View):
    def post(self, request):
        email = request.POST.get('email', '').strip()
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={'token': get_random_string(64)}
        )

        if not created and subscriber.is_active:
            return JsonResponse({'message': 'Already subscribed!'})

        if not created:
            subscriber.is_active = True
            subscriber.token = get_random_string(64)
            subscriber.save()

        messages.success(request, 'Successfully subscribed to newsletter!')
        return JsonResponse({'message': 'Subscribed successfully!'})


class UnsubscribeView(View):
    def get(self, request, token):
        subscriber = get_object_or_404(Subscriber, token=token)
        subscriber.is_active = False
        subscriber.save(update_fields=['is_active'])
        messages.success(request, 'You have been unsubscribed.')
        return redirect('news:home')
