from django.urls import path

from register_app import views

urlpatterns = [
    path('staff_home', views.staff_home, name='staff_home'),
    path('adddepartment',views.add_department,name='adddepartment'),
    path('admin', views.login_view, name='admin'),  # Ensure this view exists
    path('add_designation',views.add_designation,name='add_designation'),
    path('register_view',views.register_view,name='register_view'),
    path('view_users',views.view_users,name='view_users'),
    path('edit_user/<int:id>/', views.Edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),
    # path('create_permission/<int:id>/', views.create_permission, name='create_permission'),
    path('ajax/load-designations/', views.load_designations, name='load_designations'),
    path('logout1', views.logout_view, name='logout1'),
    path('create_permission/<int:id>', views.create_permission, name='create_permission'),
    path('user_search_export',views.user_search,name='user_search_export'),
    path('view_departmentlist',views.view_departmentlist, name='view_departmentlist'),
    path('update_departmentlist/<int:id>',views.update_departmentlist,name='update_departmentlist'),
    path('delete_departmentlist/<int:id>', views.delete_departmentlist, name='delete_departmentlist'),
    path('view_designation',views.view_designation, name='view_designation'),
    path('update_designation/<int:id>',views.update_designation,name='update_designation'),
    path('delete_designation/<int:id>', views.delete_designation, name='delete_designation'),
    path('get-submenus/<int:menu_id>/', views.get_submenus, name='get_submenus'),
]