from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from app1 import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)


urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('', views.home, name="home"),
    path('login/', views.login_view, name="login"),
    path('stock/', views.stock, name="stock"),
    path('total_stock/', views.total_stock, name="total_stock"),
    path('scan_in_1/', views.scan_in_1, name="scan_in"),
    path('scan_in/', views.add_product, name="scan_in"),
    path('addProduct/', views.add_product, name="add_product"),
    path('scan_out/', views.scan_out, name="scan_out"),
    path('scan_out_1/', views.scan_out_1, name="scan_out"),
    path('people/', views.people, name="people"),
    path('members/', views.members, name="members"),
    path('search/<q>', views.searchAjax, name="search"),
    path('p_search/<p>', views.p_search, name="p_search"),
    path('add_member/', views.add_member, name="add_member"),
    path('reports/', views.reports, name="reports"),
    path('larder_report/', views.larder_report, name="larder_report"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/',admin.site.urls),

]
 