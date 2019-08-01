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
from django.urls import path
from base import views, account_views, admin_panel_views, products_views, registration_views

urlpatterns = [
    path('', views.index_page, name="index"),
    path('login/', registration_views.user_login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('sign_up/', registration_views.sign_up_page, name="sign_up"),
    path('profile/<id>', account_views.profile_page, name="profile"),
    path('catalog/<page>', products_views.catalog_page, name='catalog'),
    path('product/<id>', products_views.product_page, name="product"),
    path('search/', products_views.search_page, name="search"),
    path('upload/', account_views.upload_file, name="upload"),
    path('settings/', account_views.account_settings_page, name="settings"),
    path('create_order/<id>', views.create_order_page, name="create_order"),
    path('orders_list/<id>', views.orders_list_page, name="orders_list"),
    path('show_order/<id>', views.show_order_page, name="show_order"),
    path('main_panel/', admin_panel_views.admin_main_panel_page, name="admin_panel"),
    path('products_panel/<page>', admin_panel_views.admin_products_panel_page, name="products_panel"),
    path('orders_panel/<page>', admin_panel_views.admin_orders_panel_page, name="orders_panel"),
    path('comments_panel/<page>', admin_panel_views.admin_comments_panel_page, name="comments_panel"),
    path('admins_panel/<page>', admin_panel_views.admin_admins_panel_page, name="admins_panel"),
    path('create_product/', products_views.create_product_page, name="create_product"),
    path('edit_product/<id>', products_views.edit_product_page, name="edit_product"),
    path('appoint_admin/<id>', account_views.admin_appoint_page, name="admin_appoint"),
    path('404/', views.not_found_page, name="404"),
    path('permission_error/', views.permission_error_page, name="permission_error"),
    path('account_banned/<username>', registration_views.account_banned_page, name="account_banned"),
    path('create_comment/<product_id>', views.create_comment_page, name="create_comment"),
    path('delete_comment/<comment>', views.delete_comment_page, name="delete_comment"),
    path('measurement_manual', views.measurement_manual_page, name="measurement_manual"),
]

handler404 = 'base.views.not_found_page'
handler500 = 'base.views.server_error_page'
