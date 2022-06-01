from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import BatchView, CategoryView, LoginToken, ProductView, RequesitionView, UserGroupView,DashboardView, RecentFiveRequestView, RecentFiveBatchView

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
    path('dashboard/', DashboardView.as_view()),
    path('request/recent/', RecentFiveRequestView.as_view()),
    path('batch/recent/', RecentFiveBatchView.as_view()),
] + router.urls