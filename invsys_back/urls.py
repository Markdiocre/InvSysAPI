from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CategoryView, GetAllCategoryView, GetAllInventoryView, GetAllProductView, InventoryView, LoginToken, MonthReportView, ProductView, QuarterlyReportView, RequesitionView, UserGroupView,DashboardView, RecentInventoryView, RecentProductView, RecentRequestView, YearlyReportView, GetAllUserGroupView

router = DefaultRouter()
router.register('category', CategoryView)
router.register('user-group',UserGroupView)
router.register('product',ProductView)
router.register('inventory',InventoryView)
router.register('request',RequesitionView)

urlpatterns = [
    path('auth/',include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    #Updates Login
    path('api-token-auth/', LoginToken.as_view()),


    #Dashboard Endpoints
    path('dashboard/', DashboardView.as_view()),
    path('request/recent/', RecentRequestView.as_view()),
    path('inventory/recent/', RecentInventoryView.as_view()),
    path('product/recent/', RecentProductView.as_view()),

    #Creation endpoints, Loads all instead of paginated
    path('inventory/all/', GetAllInventoryView.as_view()),
    path('product/all/', GetAllProductView.as_view()),
    path('category/all/', GetAllCategoryView.as_view()),
    path('user-group/all/', GetAllUserGroupView.as_view()),

    #reports
    path('monthly/', MonthReportView.as_view()),
    path('quarterly/', QuarterlyReportView.as_view()),
    path('yearly/', YearlyReportView.as_view()),


] + router.urls
