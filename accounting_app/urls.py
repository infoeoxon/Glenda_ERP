from django.urls import path

from accounting_app import views

urlpatterns = [
    path('create_voucher', views.create_voucher, name='create_voucher'),
    path('add_ledger', views.add_ledger, name='add_ledger'),
    path('ledgers', views.ledger_list, name='ledger_list'),
    path('voucher/<int:voucher_id>/', views.voucher_detail, name='voucher_detail'),
    path('vouchers', views.voucher_list, name='voucher_list'),
    path('add_group', views.add_group, name='add_group'),
    path('add_client_ledger_group', views.add_client_ledger_group, name='add_client_ledger_group'),

]