from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User, auth
from .models import Contact, Blog, Image, Category, Tag, Comment
from .forms import CommentForm, ContactForm, EditBlog, TagsForm
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.dates import DayArchiveView, YearArchiveView, MonthArchiveView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

class TagsCreateView(CreateView):
    model = Tag
    form_class = TagsForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please Authorize your identity for Add Tag")
            return redirect('/blog/login')
        return super(TagsCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['formType'] = "Create"
        return context

    def form_valid(self, form):
        messages.success(self.request,'Voila .! Data Added Successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request,'Whoops .! Data not Added.')
        return super().form_invalid(form)

class TagsUpdateView(UpdateView):
    model = Tag
    form_class = TagsForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please Authorize your identity for Update Tags")
            return redirect('/blog/login')
        return super(TagsUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['formType'] = "Update"
        return context

    def form_valid(self, form):
        messages.success(self.request,'Voila .! Data updated Successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request,'Whoops .! Data not updated.')
        return super().form_invalid(form)

    def get_object(self):
        return Tag.objects.get(id=self.kwargs.get("id"))

    def get_absolute_url(self):
        return reverse('Tags')

class TagsDeleteView(DeleteView):
    model = Tag
    template_name = "blog/tag_form.html"
    success_url = reverse_lazy('Tags')
    initial = {"methodnm"}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please Authorize your identity for Delete Tags")
            return redirect('/blog/login')
        return super(TagsDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['formType'] = "Delete"
        return context

    def form_valid(self, form):
        messages.success(self.request,'Voila .! Data Delted Successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request,'Whoops .! Data not updated.')
        return super().form_invalid(form)

    def get_object(self):
        return Tag.objects.get(id=self.kwargs.get("id"))

class TagsListView(ListView):
    model = Tag
    template_name = "blog/my_template_name.html"
    ordering = ['name']
    context_object_name = "tagData"

    def get_queryset(self):
        return Tag.objects.order_by("-id").all()

class TagsYearArchiveView(YearArchiveView):
    queryset = Tag.objects.all()
    template_name = "blog/tag_list.html"
    date_field = "created_at"
    allow_future = True
    make_object_list = True
    context_object_name = "tagData"

class TagsMonthArchiveView(MonthArchiveView):
    queryset = Tag.objects.all()
    template_name = "blog/tag_list.html"
    date_field = "created_at"
    month_format = '%m'
    allow_future = True
    make_object_list = True
    context_object_name = "tagData"

class TagsDayArchiveView(DayArchiveView):
    queryset = Tag.objects.all()
    template_name = "blog/tag_list.html"
    date_field = "created_at"
    allow_future = True
    make_object_list = True
    month_format = '%m'
    context_object_name = "tagData"

def handleSignin(request):
    if request.user.is_authenticated:
        redirect('/blog')

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '':
            messages.error(request,'Please enter username!')
            return render(request, 'login.html')
        if password == '':
            messages.error(request,'Please enter password!')
            return render(request, 'login.html')
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/blog/myblogs')
            else:
                messages.error(request,'Incorrect username or password!')
                return render(request, 'blog/login.html')
    else:
        return render(request, 'blog/login.html')

def handleLogout(request):
    auth.logout(request)
    return redirect('/blog/login')

def handleSignup(request):
    if request.method=='POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if len(email)<10:
            messages.error(request, " Your email is not valid")
            return render(request, 'blog/register.html')

        if len(fname)<2  or len(lname)<2:
            messages.error(request, " First,Last Name Should be proper")
            return render(request, 'blog/register.html')

        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return render(request, 'blog/register.html')

        if not User.objects.filter(username=email, email=email ).exists():
            myuser = User.objects.create_user(first_name=fname, last_name=lname, username=email, email=email, password=pass1)
            #########SEND EMAIL CODE#########
            plaintext = get_template('email_register.html')
            htmly     = get_template('email_register.html')
            baseurl = request.build_absolute_uri()
            d = { 
                'first_name': fname,
                'last_name': lname,
                'username': email,
                'password': pass1,
                'baseurl': baseurl,
            }
            subject, from_email, to = 'Your Registration is successful', 'admin@webblogapp.com', email
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            myuser.save()
            messages.success(request, "You are Registered successfully !")
            return redirect('/blog/login')
        else:
            messages.error(request, "Whoops .! Username/Email Already in use .!")
            return render(request, 'blog/register.html')
    else:
        return render(request, 'blog/register.html')

def index(request):
    page_number = request.GET.get('page', 1)
    searchTitle = request.GET.get('searchTitle', '')
    searchCat = request.GET.get('searchCat', '')
    catData = Category.objects.all().order_by('-id')

    if searchTitle or searchCat:
        blogs = Blog.objects.filter(title__icontains=searchTitle, is_published=1)
        if searchCat:
            blogs = Blog.objects.filter(
                title__icontains=searchTitle,
                category=searchCat,
                is_published=1
            ).order_by('-id')
    else:
        blogs = Blog.objects.filter(is_published=1).order_by('-id')

    for singleblog in blogs:
        blogsImg = Image.objects.filter(blog_id=singleblog.id).first()
        singleblog.blog_imgs = ""
        if blogsImg:
            singleblog.blog_imgs = blogsImg

    paginator = Paginator(blogs, 10)
    page_obj = paginator.get_page(page_number)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    params = {
        'blogData': page_obj,
        'countCurrent': len(page_obj),
        'count':len(blogs),
        'catData':catData,
        'searchTitle':searchTitle,
        'searchCat':searchCat,
    }
    return render(request, 'blog/index.html', params)

def myindex(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please Login to Add/Update blog")
        return redirect('/blog/login')

    page_number = request.GET.get('page')
    searchTitle = request.GET.get('searchTitle', '')
    searchCat = request.GET.get('searchCat', '')
    searchStatus = request.GET.get('searchStatus', '')
    catData = Category.objects.all().order_by('-id')

    d = {"user_id":request.user.id}
    if searchTitle or searchCat or searchStatus:
        if searchTitle:
            d.update({"title__icontains": searchTitle})
        if searchCat:
            d.update({"category": searchCat})
        if searchStatus:
            d.update({"is_published": searchStatus})
    
    blogs = Blog.objects.filter(**d).order_by("-id")

    for singleblog in blogs:
        blogsImg = Image.objects.filter(blog_id=singleblog.id).first()
        singleblog.blog_imgs = ""
        if blogsImg:
            singleblog.blog_imgs = blogsImg

    paginator = Paginator(blogs, 10)
    page_obj = paginator.get_page(page_number)
    params = {
        'blogData': page_obj,
        'countCurrent': len(page_obj),
        'count': len(blogs),
        'catData': catData,
        'searchTitle': searchTitle,
        'searchCat': searchCat,
        'searchStatus': searchStatus,
    }
    return render(request, 'blog/my-index.html', params)

class viewBlog(DetailView):
    model = Blog
    template_name = "blog/view.html"
    context_object_name = "blogData"

    def get_context_data(self, *args, **kwargs):
        blog  = Blog.objects.get(id=self.kwargs.get("pk"))
        tagCls = ['danger', 'warning', 'info', 'default', 'success']
        
        context = super().get_context_data(*args, **kwargs)
        context['tagClass'] = tagCls,
        context['blogTags'] = blog.tags.all(),
        context['blogsImg'] = Image.objects.filter(blog=blog),
        context['commentData'] = Comment.objects.filter(blog=blog),
        context['commentForm'] = CommentForm
        return context
    
    def post(self, request, *args, **kwargs):
        blogId = self.kwargs.get("pk")
        if not request.user.is_authenticated:
            messages.error(request, "Please Login to Add Comment")
            return redirect('/blog/view/' + blogId)
        # Add Comment to DB
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = User.objects.get(id=request.user.id)
            obj.blog = Blog.objects.get(id=blogId)
            obj.save()
            messages.success(request, "Comment Added successfully")
            return redirect('/blog/view/' + blogId)
        else:
            messages.error(request, "Comment cannot be added blank")
            return redirect('/blog/view/' + blogId)

def addblog(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please Login to Add/Update blog")
        return redirect('/blog/login')
        
    if request.method=='POST':
        category = request.POST['category']
        blog_tags = request.POST.getlist('blog_tags',[])
        form = EditBlog(request.POST, request.FILES)
        params = {
            'formSkelton': form,
            'action': "Add"
        }
        
        if form.is_valid():
            messages.success(request, 'Blog '+ request.POST['title'] +' Successfully.')
            obj = form.save(commit=False)
            obj.user = User.objects.get(id=request.user.id)
            obj.category = Category.objects.get(id=category)
            obj.save()
            objId = Blog.objects.latest('id') # To Get Last Inserted Id

            for img in request.FILES.getlist('blog_img'):
                Image.objects.create(blog_id=objId.id, user_id=request.user.id, name='', path=img)
            if len(blog_tags)>0:
                for tag in blog_tags:
                    obj.tags.add(tag)
            
            return redirect('/blog/myblogs')
        else:
            messages.error(request, form.errors)
            return render(request, 'blog/edit.html', params)
    else:
        params = {'formSkelton': EditBlog(),'action': "Add"}
        return render(request, 'blog/edit.html', params)

def editblog(request, id):
    blogs = Blog.objects.get(id=id)
    blogsImg = Image.objects.filter(blog=blogs)
    if not request.user.is_authenticated:
        messages.error(request, "Please Login to Add/Update blog")
        return redirect('/blog/login')
    if request.user.id != blogs.user.id:
        messages.error(request, "Authorization failed. You cannot edit someone else's blog")
        return redirect('/blog/')

    if request.method=='POST':
        category = request.POST['category']
        blog_tags = set(request.POST.getlist('blog_tags'))
        title = request.POST['title']
        description = request.POST['description']
        is_published = request.POST['is_published']
        blog = Blog.objects.get(id=id)
        if request.FILES:
            blog_img = request.FILES['blog_img']
            # This line will remove all files and add new files to code
            # Image.objects.filter(blog=id).delete()
            for img in request.FILES.getlist('blog_img'):
                Image.objects.create(blog_id=id, user_id=request.user.id, name='', path=img)
        # ---------------Method - 1 {For save form data}---------------
        # blog = Blog.objects.filter(blog_id=id, category=category, title = title, description = description)
        # blog.save()
        
        # ---------------Method - 2 {For save form data}---------------
        blog.category=Category.objects.get(id=category)
        tagsData = Tag.objects.filter(pk__in=blog_tags)
        blog.tags.clear()
        for tagInstance in tagsData:
            blog.tags.add(tagInstance)

        blog.title = title
        blog.description = description
        blog.is_published = is_published
        if request.FILES:
            blog.blog_img = blog_img
        blog.save()
        messages.success(request, 'Blog Updated Successfully.')
        return redirect('/blog/myblogs')
    else:
        
        params = {
                'blogData': blogs,
                'action': "Edit",
                'blog_tags': blogs.tags.values('id'),
                'blogsImg': blogsImg,
                'formSkelton': EditBlog({
                        'category': blogs.category,
                        'title': blogs.title,
                        'description': blogs.description,
                        'is_published': blogs.is_published
                    })
            }
        return render(request, 'blog/edit.html', params)

def removeblog(request, id):
    blogs = Blog.objects.get(id=id)
    if not request.user.is_authenticated:
        messages.error(request, "Please Login to Add/Update blog")
        return redirect('/blog/login')
    if request.user.id != blogs.user.id:
        messages.error(request, "Authorization failed. You cannot remove someone else's blog")
        return redirect('/blog/')

    blogs.delete()
    messages.success(request, 'Blog Removed Successfully.')
    return redirect('/blog/myblogs')

def removeImg(request):
    jsonObject = {}
    jsonObject["succes"] = False
    if request.method=='POST':
        imgId = request.POST['imgId']
        blogId = request.POST['blogId']
        blogImg = Image.objects.get(blog_id=blogId, id=imgId)
        if(blogImg):
            blogImg.delete()
            jsonObject["succes"] = True

    return JsonResponse(jsonObject)

def contact(request):
    params = {"contactForm": ContactForm}
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        if len(name) < 2 or len(email) < 5 or len(phone) < 10 or len(message) < 5:
            messages.error(request, 'Please provide valid details' )
            return render(request, 'blog/contact.html', params)
        else:
            contact = Contact(name=name, email=email, phone=phone, message=message)
            contact.save()
            messages.success(request, 'Form Filled Successfully. Our Team Reach you soon.')
            return redirect("/blog/contact", params)
    else:
        return render(request, 'blog/contact.html', params)
