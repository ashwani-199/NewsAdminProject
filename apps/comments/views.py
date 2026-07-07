from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from apps.comments.models import Comment, CommentLike
from apps.comments.forms import CommentForm
from apps.news.models import Article


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id, status='published')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.ip_address = request.META.get('REMOTE_ADDR')
            comment.save()
            messages.success(request, 'Comment added! It will appear after approval.')
        else:
            messages.error(request, 'Invalid comment data.')
        return redirect('news:article_detail', slug=article.slug)


class AddReplyView(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        parent = get_object_or_404(Comment, pk=comment_id, is_approved=True)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = parent.article
            comment.user = request.user
            comment.parent = parent
            comment.ip_address = request.META.get('REMOTE_ADDR')
            comment.save()
            messages.success(request, 'Reply added!')
        return redirect('news:article_detail', slug=parent.article.slug)


class EditCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated!')
        return redirect('news:article_detail', slug=comment.article.slug)


class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        article_slug = comment.article.slug
        comment.delete()
        messages.success(request, 'Comment deleted!')
        return redirect('news:article_detail', slug=article_slug)


class ReportCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        reason = request.POST.get('reason', '')
        comment.is_reported = True
        comment.report_reason = reason
        comment.save(update_fields=['is_reported', 'report_reason'])
        messages.success(request, 'Comment reported. We will review it.')
        return redirect('news:article_detail', slug=comment.article.slug)


class LikeCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if not created:
            like.delete()
            comment.likes_count = max(0, comment.likes_count - 1)
            comment.save(update_fields=['likes_count'])
            return JsonResponse({'liked': False, 'count': comment.likes_count})
        comment.likes_count += 1
        comment.save(update_fields=['likes_count'])
        return JsonResponse({'liked': True, 'count': comment.likes_count})
