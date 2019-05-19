"""SiteFM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import handler404, handler500
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from base import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index_page, name="index"),
    path('login/', views.user_login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('sign_up/', views.sign_up_page, name="sign_up"),
    path('profile/<id>', views.profile_page, name="profile"),
    path('catalog/', views.catalog_page, name='catalog'),
    path('product/<id>', views.product_page, name="product"),
    path('search/', views.search_page, name="search"),
    path('upload/', views.upload_file, name="upload"),
    path('settings/', views.account_settings_page, name="settings"),
    path('create_order/<id>', views.create_order_page, name="create_order"),
    path('orders_list/<id>', views.orders_list_page, name="orders_list"),
    path('main_panel/', views.admin_main_panel_page, name="admin_panel"),
    path('products_panel/<page>', views.admin_products_panel_page, name="products_panel"),
    path('orders_panel/', views.admin_orders_panel_page, name="orders_panel"),
    path('comments_panel/', views.admin_comments_panel_page, name="comments_panel"),
    path('admins_panel/', views.admin_admins_panel_page, name="admins_panel"),
    path('create_product/', views.create_product_page, name="create_product"),
    path('edit_product/', views.edit_product_page, name="edit_product"),
]


handler404 = 'base.views.not_found_page'
handler500 = 'base.views.server_error_page'
