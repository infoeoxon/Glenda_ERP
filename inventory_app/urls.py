

from django.urls import path

from inventory_app import views

urlpatterns = [
    path('Raw_materials_view', views.raw_materials_view, name='Raw_materials_view'),
    path('update_stocks/<int:id>', views.update_stocks, name='update_stocks'),
    path('finishedgoods_stock_view', views.finishedgoods_stock_view, name='finishedgoods_stock_view'),
    path('update_finished_goods_stocks/<int:id>', views.update_finished_goods_stocks, name='update_finished_goods_stocks'),
    path('finishedgoods_stock_history/<int:id>', views.finishedgoods_stock_history, name='finishedgoods_stock_history'),
    path('finishedgoods_stock_history/<int:id>', views.finishedgoods_stock_history, name='finishedgoods_stock_history'),
    path('damagedgoods_stock_view', views.damagedgoods_stock_view, name='damagedgoods_stock_view'),
    path('update_damaged_goods_stocks/<int:id>', views.update_damaged_goods_stocks, name='update_damaged_goods_stocks'),
    path('finishedgoods_stock_history_pdf/<int:id>', views.finishedgoods_stock_history_pdf, name='finishedgoods_stock_history_pdf'),
    path('finishedgoods_stock_history_csv/<int:id>', views.finishedgoods_stock_history_csv, name='finishedgoods_stock_history_csv'),
    path('raw_materials_stock_history/<int:id>', views.raw_materials_stock_history, name='raw_materials_stock_history'),
    path('raw_materials_history_pdf/<int:id>', views.raw_materials_stock_pdf, name='raw_materials_history_pdf'),
    path('damagedgoods_stock_history/<int:id>',views.damagedgoods_stock_history,name='damaged_good_stock_history'),
    path('generate-pdf/<int:id>', views.generate_pdf, name='generate_pdf'),
    path('generate_full_pdf',views.generate_full_pdf,name='generate_full_pdf'),
    path('generate_csv/<int:id>',views.generate_csv,name='generate_csv'),
    path('generate_excel',views.generate_excel,name='generate_excel'),
    path('search',views.search,name='search'),
    path('finishedgoods_search',views.finishedgoods_search,name='finishedgoods_search'),
    path('finishedgoods_message_request',views.finishedgoods_message_request,name='finishedgoods_message_request'),
    path('damaged_search',views.damaged_search,name='damaged_search'),
    path('raw_material_search', views.raw_material_search, name='raw_material_search'),
    path('raw_material_message_request', views.raw_material_message_request, name='raw_material_message_request'),

]

