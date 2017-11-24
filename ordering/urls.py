from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import(
    login,
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
)
from ordering import views


urlpatterns = [
    # /ordering/
    url(r'^$', views.home, name='home'),
    url(r'add-product/$', views.InventoryCreateView.as_view(), name='create_inventory'),
    url(r'delete/product_id=(?P<inventory_id>[0-9]+)/$', views.InventoryDeleteView.as_view(), name='delete_inventory'),
    url(r'update/product_id=(?P<inventory_id>[0-9]+)/$', views.InventoryUpdateView.as_view(), name='update_inventory'),
    url(r'^detail/$', permission_required('ordering.Orders')(views.DetailView.as_view()), name='detail'),
    url(r'^inventory-menu/$', permission_required('ordering.Inventorys')(views.InventoryMenu.as_view()), name='inventory_menu'),
    url(r'^inventory-detail/product_id=(?P<inventory_id>[0-9]+)/$', views.inventory_detail, name='inventory_detail'),
    url(r'^order-create/$', views.OrderCreateView.as_view(), name='order_create'),
    url(r'^order-update/order_id=(?P<order_id>[0-9]+)/$', views.OrderUpdateView.as_view(), name='order_update'),
    url(r'^order-delete/order_id=(?P<order_id>[0-9]+)/$', views.OrderDeleteView.as_view(), name='order_delete'),
    url(r'^order-successful/$', views.OrderSuccess.as_view(), name='order_success'),
    url(r'^order-history/$', views.HistoryView.as_view(), name='order_history'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register-sucess/$', views.register_success, name='register_success'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^reset-password/$', password_reset, {'template_name': 'user_account/reset_password.html', 'post_reset_redirect': 'ordering:password_reset_done', 'email_template_name': 'user_account/reset_password_email.html'}, name='reset_password'),
    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'user_account/reset_password_done.html'}, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'user_account/reset_password_confirm.html', 'post_reset_redirect': 'ordering:password_reset_complete'}, name='password_reset_confirm'),
    url(r'^reset-password/complete/$', password_reset_complete, {'template_name': 'user_account/reset_password_complete.html'}, name='password_reset_complete')
]
