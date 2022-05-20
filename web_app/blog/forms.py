from django import forms
from .models import Blog, Category, Tag, Comment

class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    name = forms.CharField(label='Enter Your Name', max_length=100)
    email = forms.CharField(label='Enter Your Email', max_length=100)
    phone = forms.CharField(label='Enter Your Mobile', max_length=10)
    message = forms.CharField(label='Enter Your Message', widget=forms.Textarea)

class TagsForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(TagsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Tag
        fields = ('name', 'status')

class EditBlog(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(EditBlog, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name != 'blog_img':
                visible.field.widget.attrs['class'] = 'form-control'
                visible.field.widget.attrs['autocomplete'] = 'off'
            if visible.name == 'is_published':
                visible.field.widget.attrs['class'] = ''

        self.fields['category'].error_messages.update({'required': 'Please select Category for Blog',})
        self.fields['title'].error_messages.update({'required': 'Please add nice Title for Blog',})
        self.fields['description'].error_messages.update({'required': 'Please add eyecatching Description for Blog',})

    class Meta:
        model = Blog
        fields = ('category', 'blog_tags', 'title', 'description', 'blog_img', 'is_published')

    category = forms.ModelChoiceField(
        required=True,
        queryset=Category.objects.all().order_by('-id'), 
        widget=forms.Select(attrs={'class': "form-control"}), 
    )
    blog_tags = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Tag.objects.all().order_by('-id'),
        widget=forms.SelectMultiple(attrs={
            'multiple':'true',
            'class': "form-control"
            }), 
    )
    is_published = forms.ChoiceField(choices=[('1','Yes'),('0','No')], widget=forms.RadioSelect)
    # title = forms.CharField(label='Enter Blog Title', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    # description = forms.CharField(label='Enter Blog Descritpion', widget=forms.Textarea(attrs={'class': "form-control"}))
    blog_img = forms.ImageField(
        label='Select Blog Image',
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = ('title', )
        labels = {
            "title": "Enter Your Comment"
        }
