from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView, DetailView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView, HitCountMixin

from .models import News, Category, Comment
from .forms import ContactForm, CommentForm
from news_project.custom_permissions import OnlyLoggedSuperUser

# Create your views here.

def news_list(request):
    news_list = News.published.all() # 1-usul
#    news_list = News.objects.filter(status=News.Status.Published) # 2-usul
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)


class NewsDetailView(HitCountDetailView):
    model = News
    count_hit = True
    template_name = 'news/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.get_object()
        # news.view_count = news.view_count + 1 # birinchi usul har bir update da qushib boraveradi
        # news.save() # bu xato
        comments = news.comments.filter(active=True)
        comment_count = comments.count
        comment_form = CommentForm()
        context['news'] = news
        context['comment_count'] = comment_count
        context["comments"] = comments
        context["comment_form"] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        news = self.get_object()
        comments = news.comments.filter(active=True)
        comment_count = comments.count
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            # comment_form = CommentForm() #reverse qilingand an keyin bu kerak bo'lmadi

        else:
            new_comment = None

        return redirect(reverse('news_detail_page', kwargs={'slug': news.slug}))

# @login_required
def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #yangi komment obyektini yaratamiz lekin DB ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            #izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            #ma'lumotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form = CommentForm() #formadan kiritilgan malumotni rest yani tozalb yuborish
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        "comments": comments,
        "new_comment":new_comment,
        "comment_form": comment_form
    }
    return render(request, 'news/news_detail.html', context)

def homePageView(request):
    categories = Category.objects.all()
    news_list = News.published.all().order_by('-publish_time')[:5]
    local_one = News.published.filter(category__name="Mahalliy").order_by("-publish_time")[:1]
    local_news = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[1:5]
    context = {
        'news_list': news_list,
        "categories": categories,
        "local_news": local_news,
        "local_one": local_one
    }
    return render(request, 'news/home.html', context)

class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:15]
        # context['local_one'] = News.published.filter(category__name="Mahalliy").order_by("-publish_time")[:1]
        # context['local_news'] = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[1:5]
        context['mahalliy_xabarlar'] = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[:5]
        context['xorij_xabarlar'] = News.published.all().filter(category__name="Xorij").order_by("-publish_time")[:5]
        context['texnologiya_xabarlar'] = News.published.all().filter(category__name="Texnologiya").order_by("-publish_time")[:5]
        context['sport_xabarlar'] = News.published.all().filter(category__name="Sport").order_by("-publish_time")[:5]
        return context

class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Xorij").order_by("-publish_time")
        return news

class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologiya_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Texnologiya").order_by("-publish_time")
        return news

class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Sport").order_by("-publish_time")
        return news

# funksiya orqali ishlatish
# def contactPageView(request):
#     print(request.POST)
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur! </h2>")
#     context = {
#         "form": form
#     }
#     return render(request, 'news/contact.html', context)

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur!!!</h2>")
        context = {
            'form': form
        }

        return render(request, 'news/contact.html', context)

def errorPageView(request):
    context = {

    }
    return render(request, 'news/404.html', context)

def aboutPageView(request):
    context = {

    }
    return render(request, 'news/about.html', context)

class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'slug', 'body', 'image', 'category', 'status', )
    template_name = 'crud/news_edit.html'

    def form_valid(self, form):
        self.News = form.save(commit=False)

        if not self.News.slug:
            self.News.slug = slugify(self.News.title)

        self.News.save()

        return super().form_valid(form)

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')

    def form_valid(self, form):
        self.News = form.save(commit=False)

        if not self.News.slug:
            self.News.slug = slugify(self.News.title)

        self.News.save()

        return super().form_valid(form)

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')
    # login_url = 'login' settings.py da hamm classlar uchun bitt yozilgan LOGIN_URL = 'login'

    def test_func(self):
        return self.request.user.is_superuser # buni o'rniga custom_permissions dan OnlyLoggedSuperUser ni ishlatsa ham bo'ladi

@login_required()
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)

class SearchResultsList(ListView):
    model = News
    template_name = 'news/serch_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )