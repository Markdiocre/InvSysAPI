from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import BatchView, CategoryView, LoginToken, ProductView, RequesitionView, UserGroupView

router = DefaultRouter()
router.register('category', CategoryView)
router.register('user-group',UserGroupView)
router.register('product',ProductView)
router.register('batch',BatchView)
router.register('request',RequesitionView)

urlpatterns = [
    path('auth/',include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    #Updates Login
    path('api-token-auth/', LoginToken.as_view()),
] + router.urls