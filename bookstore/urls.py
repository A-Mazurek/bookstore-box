from django.contrib import admin
from django.urls import path
from bookstore_statistics.views import bookstore_summary


urlpatterns = [
    path('api/summary/<str:flag>', bookstore_summary),
    path('admin/', admin.site.urls),
]
