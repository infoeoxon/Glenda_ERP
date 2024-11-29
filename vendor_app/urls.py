from django.urls import path

from vendor_app import views

urlpatterns = [
    path('vender_register_view', views.vender_register_view, name='vender_register_view'),
    path('view_customers_list', views.view_customers_list, name='view_customers_list'),
    path('create_vendor_details/<int:id>', views.create_vendor_details, name='create_vendor_details'),
    path('view_vendor_profile/<int:id>', views.view_vendor_profile, name='view_vendor_profile'),
    path('export_vendor_profile_pdf/<int:id>', views.vendor_details_pdf, name='export_vendor_profile_pdf'),
    path('export_vendor_list_csv', views.vendor_list_csv, name='export_vendor_list_csv'),
    path('view_vendors', views.view_vendors, name='view_vendors'),
    path('vendor/details/<int:vendor_id>/', views.vendor_details, name='vendor_details'),

    # path('vendor_search',views.vendor_search,name='vendor_search'),
    path('edit_vender/<int:id>', views.edit_vender, name='edit_vender'),
    path('delete_vender_view/<int:id>', views.delete_vender_view, name='delete_vender_view'),
    # vendor front page
    path('login', views.vendor_login, name='login'),
    path('vendor_search_and_export',views.vendor_search_and_export,name='vendor_search_and_export'),
    path('signup', views.signup, name='signup'),
    path('request', views.request, name='request'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('front_logout', views.front_logout, name='front_logout'),
    path('vendor_request', views.vendor_request_list, name='vendor_request'),
    path('approve_as_vendor/<int:id>', views.approve_as_vendor, name='approve_as_vendor'),
    # path('approve_as_distributor/<int:id>', views.approve_as_distributor, name='approve_as_distributor'),
    path('approve_as_customer/<int:id>', views.approve_as_customer, name='approve_as_customer'),
    path('vendor_verification', views.vendor_verification, name='vendor_verification'),
    path('approve_as_vendor_details/<int:id>',views.approve_as_vendor_details,name='approve_as_vendor_details')

]
