from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LaptopViewSet, CategoryViewSet, LikedLaptoptView


router = DefaultRouter()
router.register('laptops', LaptopViewSet, 'laptops')
router.register('categories', CategoryViewSet, 'category')


urlpatterns = [
    path('liked/', LikedLaptoptView.as_view(), name='liked')
]

urlpatterns += router.urls