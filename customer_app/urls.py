from django.urls import path
from customer_app import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('certificate', views.Certificate, name='certificate'),
    path('quality', views.quality, name='quality'),
    path('steps', views.Steps, name='steps'),

    path('view_customeruser',views.view_customeruser, name='view_customeruser'),
    path('customer_search',views.customer_search,name='customer_search'),
    path('view_customer_profile/<int:id>', views.view_customer_profile, name='view_customer_profile'),
    path('customer_exportsearch', views.customer_exportsearch, name='customer_exportsearch'),
    path('view_dealers', views.view_dealers, name='view_dealers'),
    path('customer/details/<int:customer_id>/', views.get_customer_details, name='customer_details'),
    path('create_customer_details/<int:id>', views.create_customer_details, name='create_customer_details'),

]