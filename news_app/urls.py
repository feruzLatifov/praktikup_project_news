from django.urls import path
from .views import news_list, news_detail, homePageView, ContactPageView, errorPageView, aboutPageView, \
    HomePageView, LocalNewsView, ForeignNewsView, TechnologyNewsView, SportNewsView, NewsUpdateView, \
    NewsDeleteView, NewsCreateView, admin_page_view, NewsDetailView, SearchResultsList

urlpatterns = [
    # path('', homePageView, name='home_page'),
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', news_list, name="all_news_list"),
    path('news/create/', NewsCreateView.as_view(), name="news_create"),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('local/', LocalNewsView.as_view(), name="local_news_page"),
    path('foreign/', ForeignNewsView.as_view(), name="foreign_news_page"),
    path('technology/', TechnologyNewsView.as_view(), name="technology_news_page"),
    path('sport/', SportNewsView.as_view(), name="sport_news_page"),
    # path('news/<slug:news>/', news_detail, name="news_detail_page"),
    path('news/<slug>/', NewsDetailView.as_view(), name="news_detail_page"),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('about/', aboutPageView, name='about_page'),
    path('404/', errorPageView, name='404_page'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresult/', SearchResultsList.as_view(), name='search_result'),
]