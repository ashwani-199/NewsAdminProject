from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from apps.news.models import Article, Category, Like, Bookmark
from apps.news.forms import ArticleForm
from apps.comments.models import Comment
from apps.notifications.models import Notification
from apps.newsletter.models import Subscriber
from apps.core.models import ContactMessage, WebsiteSettings
from apps.accounts.models import User, AuthorIDCard


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_journalist or self.request.user.can_publish


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.role == 'administrator'


class AuthorDashboardView(LoginRequiredMixin, AuthorRequiredMixin, View):
    template_name = 'author_dashboard/dashboard.html'

    def get(self, request):
        articles = Article.objects.filter(author=request.user)
        context = {
            'total_articles': articles.count(),
            'published_articles': articles.filter(status='published').count(),
            'draft_articles': articles.filter(status='draft').count(),
            'total_views': articles.aggregate(total=Sum('views_count'))['total'] or 0,
            'total_likes': articles.aggregate(total=Sum('likes_count'))['total'] or 0,
            'recent_articles': articles.order_by('-created_at')[:5],
        }
        return render(request, self.template_name, context)


class AuthorArticlesView(LoginRequiredMixin, AuthorRequiredMixin, View):
    template_name = 'author_dashboard/articles.html'

    def get(self, request):
        articles = Article.objects.filter(author=request.user).select_related('category')
        status = request.GET.get('status', '')
        if status:
            articles = articles.filter(status=status)
        return render(request, self.template_name, {'articles': articles, 'current_status': status})


class CreateArticleView(LoginRequiredMixin, AuthorRequiredMixin, View):
    template_name = 'author_dashboard/article_form.html'

    def get(self, request):
        form = ArticleForm()
        return render(request, self.template_name, {'form': form, 'is_create': True})

    def post(self, request):
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            if article.status == 'published':
                article.published_at = timezone.now()
            article.save()
            form.save_m2m()
            messages.success(request, 'Article created successfully!')
            return redirect('dashboard:author_articles')
        return render(request, self.template_name, {'form': form, 'is_create': True})


class EditArticleView(LoginRequiredMixin, AuthorRequiredMixin, View):
    template_name = 'author_dashboard/article_form.html'

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug, author=request.user)
        form = ArticleForm(instance=article)
        return render(request, self.template_name, {'form': form, 'article': article, 'is_create': False})

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug, author=request.user)
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            if article.status == 'published' and not article.published_at:
                article.published_at = timezone.now()
            article.save()
            form.save_m2m()
            messages.success(request, 'Article updated successfully!')
            return redirect('dashboard:author_articles')
        return render(request, self.template_name, {'form': form, 'article': article, 'is_create': False})


class DeleteArticleView(LoginRequiredMixin, AuthorRequiredMixin, View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk, author=request.user)
        article.delete()
        messages.success(request, 'Article deleted.')
        return redirect('dashboard:author_articles')


class AuthorStatsView(LoginRequiredMixin, AuthorRequiredMixin, View):
    template_name = 'author_dashboard/stats.html'

    def get(self, request):
        articles = Article.objects.filter(author=request.user)
        context = {
            'total_articles': articles.count(),
            'total_views': articles.aggregate(total=Sum('views_count'))['total'] or 0,
            'total_likes': articles.aggregate(total=Sum('likes_count'))['total'] or 0,
            'articles_by_status': articles.values('status').annotate(count=Count('id')),
            'articles_by_category': articles.values('category__name').annotate(count=Count('id')),
        }
        return render(request, self.template_name, context)


class AdminDashboardView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'admin_dashboard/dashboard.html'

    def get(self, request):
        now = timezone.now()
        context = {
            'total_users': User.objects.count(),
            'total_articles': Article.objects.count(),
            'published_articles': Article.objects.filter(status='published').count(),
            'total_categories': Category.objects.count(),
            'total_comments': Comment.objects.count(),
            'pending_comments': Comment.objects.filter(is_approved=False).count(),
            'total_subscribers': Subscriber.objects.count(),
            'total_messages': ContactMessage.objects.count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
            'recent_articles': Article.objects.order_by('-created_at')[:5],
            'recent_comments': Comment.objects.order_by('-created_at')[:5],
            'recent_users': User.objects.order_by('-date_joined')[:5],
        }
        return render(request, self.template_name, context)


class AdminUsersView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'admin_dashboard/users.html'

    def get(self, request):
        q = request.GET.get('q', '')
        role = request.GET.get('role', '')
        users = User.objects.all()
        if q:
            users = users.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(first_name__icontains=q))
        if role:
            users = users.filter(role=role)
        return render(request, self.template_name, {'users': users})


class AdminAuthorsView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'admin_dashboard/authors.html'

    def get(self, request):
        authors = User.objects.filter(role='journalist').annotate(
            article_count=Count('articles')
        )
        return render(request, self.template_name, {'authors': authors})


class AdminArticlesView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'admin_dashboard/articles.html'

    def get(self, request):
        q = request.GET.get('q', '')
        status = request.GET.get('status', '')
        articles = Article.objects.select_related('author', 'category').all()
        if q:
            articles = articles.filter(title__icontains=q)
        if status:
            articles = articles.filter(status=status)
        return render(request, self.template_name, {'articles': articles})


class AdminCommentsView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'admin_dashboard/comments.html'

    def get(self, request):
        comments = Comment.objects.select_related('user', 'article').all()
        return render(request, self.template_name, {'comments': comments})


class AdminCategoriesView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'admin_dashboard/categories.html'

    def get(self, request):
        categories = Category.objects.annotate(article_count=Count('articles'))
        return render(request, self.template_name, {'categories': categories})


class AdminSubscribersView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'admin_dashboard/subscribers.html'

    def get(self, request):
        subscribers = Subscriber.objects.all()
        return render(request, self.template_name, {'subscribers': subscribers})


class AdminMessagesView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'admin_dashboard/messages.html'

    def get(self, request):
        messages_list = ContactMessage.objects.all()
        return render(request, self.template_name, {'messages': messages_list})


class AdminContactMessagesView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'admin_dashboard/contacts.html'

    def get(self, request):
        contacts = ContactMessage.objects.all()
        return render(request, self.template_name, {'contacts': contacts})


class AdminSettingsView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'admin_dashboard/settings.html'

    def get(self, request):
        settings = WebsiteSettings.objects.first()
        return render(request, self.template_name, {'settings': settings})

    def post(self, request):
        settings, _ = WebsiteSettings.objects.get_or_create(pk=1)
        fields = ['site_name', 'site_tagline', 'footer_text', 'copyright_text',
                  'contact_email', 'contact_phone', 'address', 'facebook_url',
                  'twitter_url', 'instagram_url', 'youtube_url', 'linkedin_url']
        for field in fields:
            setattr(settings, field, request.POST.get(field, ''))
        if request.FILES.get('site_logo'):
            settings.site_logo = request.FILES['site_logo']
        if request.FILES.get('site_favicon'):
            settings.site_favicon = request.FILES['site_favicon']
        settings.save()
        messages.success(request, 'Settings updated!')
        return redirect('dashboard:admin_settings')


class RequestIDCardView(LoginRequiredMixin, AuthorRequiredMixin, View):
    def get(self, request):
        id_card = AuthorIDCard.objects.filter(user=request.user).first()
        context = {'id_card': id_card}
        return render(request, 'author_dashboard/id_card.html', context)

    def post(self, request):
        existing = AuthorIDCard.objects.filter(user=request.user, status='pending').exists()
        if existing:
            messages.warning(request, 'You already have a pending ID card request.')
            return redirect('dashboard:request_id_card')
        approved = AuthorIDCard.objects.filter(user=request.user, status='approved', is_active=True).exists()
        if approved:
            messages.warning(request, 'You already have an active ID card.')
            return redirect('dashboard:request_id_card')
        AuthorIDCard.objects.create(user=request.user)
        messages.success(request, 'ID card request submitted! Waiting for admin approval.')
        return redirect('dashboard:request_id_card')


class DownloadIDCardView(LoginRequiredMixin, AuthorRequiredMixin, View):
    def get(self, request):
        id_card = AuthorIDCard.objects.filter(user=request.user, status='approved', is_active=True).first()
        if not id_card:
            messages.error(request, 'No approved ID card found.')
            return redirect('dashboard:request_id_card')
        settings = WebsiteSettings.objects.first()
        avatar_url = ''
        if request.user.avatar:
            avatar_url = request.build_absolute_uri(request.user.avatar.url)
        logo_url = ''
        if settings and settings.site_logo:
            logo_url = request.build_absolute_uri(settings.site_logo.url)
        html_string = render_to_string('author_dashboard/id_card_pdf.html', {
            'id_card': id_card,
            'user': request.user,
            'site_settings': settings,
            'avatar_url': avatar_url,
            'logo_url': logo_url,
            'request': request,
        })
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="IDCard_{id_card.card_id}.pdf"'
        from xhtml2pdf import pisa
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)
        return response


class AdminApproveIDCardView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not (request.user.is_staff or request.user.role == 'administrator'):
            messages.error(request, 'Permission denied.')
            return redirect('dashboard:admin_dashboard')
        id_card = get_object_or_404(AuthorIDCard, pk=pk)
        action = request.POST.get('action')
        if action == 'approve':
            from datetime import timedelta
            id_card.status = 'approved'
            id_card.approved_at = timezone.now()
            id_card.approved_by = request.user
            id_card.expiry_date = (timezone.now() + timedelta(days=365)).date()
            id_card.save()
            messages.success(request, f'ID card {id_card.card_id} approved.')
        elif action == 'reject':
            id_card.status = 'rejected'
            id_card.rejection_reason = request.POST.get('reason', '')
            id_card.save()
            messages.success(request, f'ID card {id_card.card_id} rejected.')
        elif action == 'revoke':
            id_card.is_active = False
            id_card.save()
            messages.success(request, f'ID card {id_card.card_id} revoked.')
        return redirect('dashboard:admin_id_cards')


class AdminIDCardsView(LoginRequiredMixin, View):
    def get(self, request):
        if not (request.user.is_staff or request.user.role == 'administrator'):
            messages.error(request, 'Permission denied.')
            return redirect('dashboard:admin_dashboard')
        status = request.GET.get('status', '')
        id_cards = AuthorIDCard.objects.select_related('user', 'approved_by').all()
        if status:
            id_cards = id_cards.filter(status=status)
        context = {
            'id_cards': id_cards,
            'current_status': status,
            'pending_count': AuthorIDCard.objects.filter(status='pending').count(),
        }
        return render(request, 'admin_dashboard/id_cards.html', context)
