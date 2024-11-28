from django.urls import path

from rd_app import views

urlpatterns = [
    path('raw_material_stock_approve', views.raw_material_stock_approve, name='raw_material_stock_approve'),
    path('raw_material_stock_approve_review/<int:id>', views.raw_material_stock_approve_review, name='raw_material_stock_approve_review'),
    path('stock_approval_history/<int:id>', views.stock_approval_history,name='stock_approval_history'),
    path('raw_material_stock_approve_pdf', views.raw_material_stock_approve_pdf, name='raw_material_stock_approve_pdf'),
    path('raw_material_stock_approve_excel', views.raw_material_stock_approve_excel, name='raw_material_stock_approve_excel'),

    path('verification_list',views.verification_list, name='verification_list'),
    path('quality_check_list', views.quality_check_list, name='quality_check_list'),
    path('rd_history', views.rd_history, name='rd_history'),
    path('quality_check_history', views.quality_check_history, name='quality_check_history'),
    path('verification_history', views.verification_history, name='verification_history')
]
