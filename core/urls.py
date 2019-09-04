from django.urls import path

from core.views import HomePageView, RedirectToOriginalUrl, CRUDView, DeleteUrlView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('detail/<int:pk>/', CRUDView.as_view(), name='crud-url'),
    path('delete/<int:pk>/', DeleteUrlView.as_view(), name='delete-url'),
    path('<str:short_url>/', RedirectToOriginalUrl.as_view(), name='redirect-to-original-url'),
]
