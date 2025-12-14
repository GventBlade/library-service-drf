from rest_framework.routers import DefaultRouter
from django.urls import path, include
from books.views import BookViewSet

router = DefaultRouter()

router.register('', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

app_name = 'books'
