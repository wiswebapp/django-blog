from . import views
from django.urls import path
from django.contrib import admin

#django admin header customization
admin.site.site_header = "Login To Blog Application"
admin.site.title = "Developer Web Blog"
admin.site.index_title = "Welcome to Blog Applications"

urlpatterns = [
    path('', views.index, name='BlogHome'),
    path('view/<slug:pk>', views.viewBlog.as_view(), name='BlogView'),
    path('add/', views.addblog, name='BlogAdd'),
    path('edit/<int:id>', views.editblog, name='BlogEdit'),
    path('remove/<int:id>', views.removeblog, name='BlogRemove'),
    path('removeImg/', views.removeImg, name='BlogImgRemove'),
    path('myblogs', views.myindex, name='BlogRemove'),
    path('tags', views.TagsListView.as_view(), name='Tags'),
    path('tags/create/', views.TagsCreateView.as_view(), name='TagsCreate'),
    path('tags/edit/<int:id>', views.TagsUpdateView.as_view(), name='TagsUpdate'),
    path('tags/delete/<int:id>', views.TagsDeleteView.as_view(), name='TagsDelte'),
    path('tags/<int:year>/<int:month>/<int:day>/', views.TagsDayArchiveView.as_view(), name="archive_day"),
    path('tags/<int:year>/<int:month>/', views.TagsMonthArchiveView.as_view(), name="archive_day"),
    path('tags/<int:year>/', views.TagsYearArchiveView.as_view(), name="archive_day"),
    path('contact', views.contact, name='BlogContact'),
    path('login', views.handleSignin, name='BlogLogin'),
    path('register', views.handleSignup, name='BlogRegister'),
    path('logout', views.handleLogout, name='BlogLogout'),
]
