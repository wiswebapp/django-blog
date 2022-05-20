from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Blog, Contact, Category, Image, Tag, Comment

class MyModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
             'all': ('css/admin/template',)
        }

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    def created_on(self, obj):
        return obj.created_at.strftime("%d %b %Y")
    created_on.admin_order_field = 'created_at'

    def published_status(self, obj):
        if obj.is_published:
            return "Published"
        return "UnPublished"
    published_status.admin_order_field = 'is_published'

    def user_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
    user_name.admin_order_field = 'user'
    
    list_display = ['id', "created_on", 'user_name', 'title', 'category', 'published_status']
    list_filter = ['created_at','user','category','is_published']
    search_fields = ("title", )
    fields = ('user', 'title', 'category', 'description', 'tags', 'is_published')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if len(form.base_fields) > 0:
            form.base_fields["user"].label = "Who is Writer:"
            form.base_fields["title"].label = "Enter Title For Blog:"
            form.base_fields["category"].label = "Specify Category:"
            form.base_fields["is_published"].label = "Is Blog Published:"
            return form
        return form

# admin.site.register(Blog)
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at']
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'path', 'status']

@admin.register(Comment)
class ImageAdmin(admin.ModelAdmin):

    def added_on(self, obj):
        return obj.created_at.strftime("%d %b %Y")
    added_on.admin_order_field = 'created_at'

    # def user_name(self, obj):
    #     return format_html('<a target="_blank" href="%s">%s</a>' % ('/admin/auth/user/' + str(obj.user.id) + '/change', obj.user.first_name + " " + obj.user.last_name))
    # user_name.admin_order_field = 'user'
    
    def blog_title(self, obj):
        return format_html('<a target="_blank" href="%s">%s</a>' % ('/admin/blog/blog/' + str(obj.blog.id) + '/change', obj.blog.title))
    blog_title.admin_order_field = 'blog'

    def comment(self, obj):
        return obj.title
    comment.admin_order_field = 'title'

    list_display = ['added_on', 'user', 'blog_title', 'comment']
    list_filter = ['user', 'blog', ]
    search_fields = ("title", )