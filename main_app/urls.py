from . import views
from django.urls import path
from .views import contactView, successView, resourceView

urlpatterns = [
    path('', views.home, name='home'),
    path('resources/', views.resources_index, name='index'),

    path('contact/', contactView, name='contact'),
    path('success/', successView, name='success'),

    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    path('manage_resources/', views.manage_resources, name='resources_manage'),
    path('resources/create/', resourceView, name='resources_create'),
    path('resources/<int:pk>/update/',
         views.ResourceUpdate.as_view(), name='resources_update'),

    path('about/', views.about, name='about'),
    path('resources/categories', views.resources_categories, name='category'),
    path('accounts/signup/', views.signup, name='signup'),
    path('resources/<int:resource_id>/', views.resources_detail,
         name='detail'),
    path('resources/<int:pk>/delete/',
         views.ResourceDelete.as_view(), name='resources_delete'),
    path('myresources/', views.myresources, name='myresource'),
]
