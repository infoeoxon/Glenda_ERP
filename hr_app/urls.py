from django.urls import path
from hr_app import views
urlpatterns = [
    path('Employee_list',views.Employee_list,name='Employee_list'),
    path('AddDetails/<int:id>',views.AddDetails,name='AddDetails'),
    path('view_employee_profile/<int:id>',views.view_employee_profile,name='view_employee_profile'),
    path('update_employee_details/<int:id>',views.update_employee_details,name='update_employee_details'),
    path('delete_employee_details/<int:id>',views.delete_employee_details,name='delete_employee_details'),
    path('employee_search_and_export',views.employee_search_and_export,name='employee_search_and_export'),
]