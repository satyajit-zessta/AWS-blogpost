from django.shortcuts import redirect
from django.urls import reverse
from blogging.models import *
from django.contrib.auth import authenticate
from .forms import *
from django.template.response import TemplateResponse as render
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg, F, Func, Sum
from blogpost_project.settings import MEDIA_URL

Admin = get_user_model()
# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all(),
        'MEDIA_URL': MEDIA_URL

    }
    # num = 10/0
    return render(request, 'index.html', context)


# user informations
def user_info(request):
    usrs = User.objects.all()
    return render(request,'user.html', {'users':usrs})

def user_view(request, user_id):
    usr = User.objects.get(id = user_id)
    
    post_by_user = Post.objects.filter(author = usr)
    
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if (usr.user_name == user_name and usr.password == password):
            return render(request, 'user_view.html', {'user': usr, 'posts':post_by_user})
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'User'})
    else:
        return render(request, 'user_verification.html',  {'profile_type': 'User', 'user':usr})

# user verification
def user_verification(request, user_id):
     
    usr = User.objects.get(id = user_id)
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        if (usr.user_name == user_name and usr.password == password):
            return redirect(reverse('user_update_profile', kwargs={'user_id': usr.id}))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'User'})
    else:
        return render(request, 'user_verification.html',  {'profile_type': 'User', 'user':usr})

# user updation
def user_update_profile(request, user_id):
    usr = User.objects.get(id = user_id)
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        u_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('c_password')
        if password == usr.password:
            if f_name != usr.first_name:
                usr.first_name = f_name
            if l_name != usr.last_name:
                usr.last_name = l_name
            if u_name != usr.user_name:
                usr.user_name = u_name
            if email != usr.email:
                usr.email = email
            usr.save()
            return redirect(reverse('user_info'))
        else:
            return render(request, 'user_edit.html', {'user': usr, 'invalid_password' : True})  
    else:
        return render(request, 'user_edit.html', {'user':usr, 'invalid_password': False,'show_password':False})

# user deletion
def user_delete_profile(request, user_id):
    usr = User.objects.get(id = user_id)
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if usr.user_name == user_name and usr.password == password:
            usr.delete()
            return redirect(reverse('user_info'))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True})
    else:
        return render(request, 'user_verification.html')

# admin verification
def admin_verification(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        if authenticate(request, username=user_name, password=password) is not None:
            return redirect(reverse('add_user'))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'Admin'})
    else:
        return render(request, 'user_verification.html', {'profile_type': 'Admin'})
    
# adding user
def add_user(request):
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        u_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        user =User(first_name = f_name, last_name = l_name, user_name = u_name, email = email, password = password)
        if c_password == password:
            user.save()
            return redirect(reverse('user_info'))
        else:
            return render(request, 'user_edit.html', {'mismatch_password': True, "show_password" : True})
    else:
        return render(request, 'user_edit.html', {'mismatch_password': False,"show_password" : True})


# POST
def view_posts(request):
    posts_with_comments_count = Post.objects.annotate(num_of_comments=Count('comments'))
    avg_comments_per_post = posts_with_comments_count.aggregate(avg = Avg('num_of_comments'))['avg']

    posts_with_comments_and_word_count = posts_with_comments_count.annotate(
        word_len = Sum(
            Func(F('content'), 
                function = 'LENGTH', 
                template = '%(function)s(%(expressions)s) - LENGTH(REPLACE(%(expressions)s, " ", "")) + 1')))
    avg_words_per_post =  posts_with_comments_and_word_count.aggregate(avg_words=Avg('word_len'))['avg_words'] or 0
        
    context = {
        'posts' : posts_with_comments_and_word_count,
        'average_comments_per_post' : round(avg_comments_per_post,2),
        'average_words_per_post' : round(avg_words_per_post,2)}
    return render(request, 'post_view.html', context)

def post_info(request,post_id):
    post = Post.objects.get(id = post_id)
    return render(request, 'post_info.html', {'post':post,'MEDIA_URL': MEDIA_URL})

def update_post(request, post_id):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if authenticate(request, username=user_name, password=password) is not None:
            return redirect(reverse('edit_post', kwargs={'post_id': post_id}))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'Admin'})
    else:
        return render(request, 'user_verification.html', {'profile_type': 'Admin'})


def edit_post(request, post_id):
    post = Post.objects.get(id = post_id)
    post_form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if request.method == 'POST':
        if post_form.is_valid():
            # Save the post
            post_instance = post_form.save(commit=False)
            post_instance.save()

            # Update related tags
            tags_data = request.POST.getlist('tags')
            post_instance.tags.clear()
            for tag_id in tags_data:
                tag = Tagging.objects.get(id=tag_id)
                post_instance.tags.add(tag)
                tag.posts.add(post_instance)

            # Update related comments
            comments_data = request.POST.getlist('comments')
            post_instance.comments.clear()
            for comment_id in comments_data:
                comment = Comment.objects.get(id=comment_id)
                post_instance.comments.add(comment)
                comment.post.add(post_instance)


            post_instance.save()
            return redirect('view_posts')
    else:
        return render(request, 'post.html', {'post_form': post_form, 'Action': 'Update'})
    

def verification_for_add_post(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if authenticate(request, username=user_name, password=password) is not None:
            return redirect(reverse('add_post'))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'Admin'})
    else:
        return render(request, 'user_verification.html', {'profile_type': 'Admin'})


def add_post(request):
    post_form = PostForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_instance = post_form.save(commit=False)
            post_instance.save()

            # Update related tags
            tag_ids = request.POST.getlist('tags')
            tags = Tagging.objects.filter(id__in=tag_ids)
            post_instance.tags.set(tags)
            post_instance.tags_count = tags.count()

            # Update related comments
            comment_ids = request.POST.getlist('comments')
            comments = Comment.objects.filter(id__in=comment_ids)
            post_instance.comments.set(comments)

            # Update related objects
            for tag in tags:
                tag.posts.add(post_instance)
            for comment in comments:
                comment.post.add(post_instance)

            return redirect(reverse('view_posts'))
    return render(request, 'post.html', {'post_form': post_form, 'Action': 'Add'})

# post deletion
def delete_post(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if authenticate(request, username=user_name, password=password) is not None:
            post.delete()
            return redirect(reverse('view_posts'))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'Admin'})
    else:
        return render(request, 'user_verification.html', {'profile_type': 'Admin'})



# TAG
def view_tags(request):
    tags = Tagging.objects.all()
    return render(request, 'tags_view.html', {'tags': tags})

def delete_tag(request, tag_id):
    tag = Tagging.objects.get(id = tag_id)
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if authenticate(request, username=user_name, password=password) is not None:
            tag.delete()
            return redirect(reverse('view_tags'))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'Admin'})
    else:
        return render(request, 'user_verification.html', {'profile_type': 'Admin'})


def update_tag(request, tag_id):

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if authenticate(request, username=user_name, password=password) is not None:
            return redirect(reverse('edit_tag', kwargs={'tag_id': tag_id}))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'Admin'})
    else:
        return render(request, 'user_verification.html', {'profile_type': 'Admin'})

def edit_tag(request, tag_id):
    tag = Tagging.objects.get(id = tag_id)
    tags = TagForm(instance = tag)
    if request.method == 'POST':
        name = request.POST.get('name')

        # Many to many field
        post_ids = request.POST.getlist('posts')
        posts = Post.objects.filter(id__in=post_ids)

        tag.name = name
        tag.posts.set(posts)
        tag.save()
        for post in posts:
           tag.posts.add(post,) 
        return redirect(reverse('view_tags'))
    else:
        return render(request, 'tag_form.html',{'tag_form':tags, 'Action':'Update'}) 

def verification_for_add_tag(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if authenticate(request, username=user_name, password=password) is not None:
            return redirect(reverse('add_tag'))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'Admin'})
    else:
        return render(request, 'user_verification.html', {'profile_type': 'Admin'})

def add_tag(request):
    tags = TagForm()
    if request.method == 'POST':
        name = request.POST.get('name')

        # Many to many field
        post_ids = request.POST.getlist('posts')
        posts = Post.objects.filter(id__in=post_ids)

        tag=Tagging(name=name)
        tag.save()
        tag.posts.add(*posts)
        for post in posts:
           tag.posts.add(post,) 
        return redirect(reverse('view_tags'))
    else:
        return render(request, 'tag_form.html',{'tag_form':tags, 'Action':'Add'})


def view_comments(request):
    comments = Comment.objects.all()
    return render(request, 'comment_view.html', {'comments': comments})

def comment_info(request,comment_id):
    comment = Comment.objects.get(id = comment_id)
    return render(request, 'comment_info.html', {'comment':comment})

def delete_comment(request, comment_id):
    comment = Comment.objects.get(id = comment_id)
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if authenticate(request, username=user_name, password=password) is not None:
            comment.delete()
            return redirect(reverse('view_comments'))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'Admin'})
    else:
        return render(request, 'user_verification.html', {'profile_type': 'Admin'})



def update_comment(request, comment_id):

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if authenticate(request, username=user_name, password=password) is not None:
            return redirect(reverse('edit_comment', kwargs={'comment_id': comment_id}))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'Admin'})
    else:
        return render(request, 'user_verification.html', {'profile_type': 'Admin'})

def edit_comment(request, comment_id):
    comment = Comment.objects.get(id = comment_id)
    comments = CommentForm(instance = comment)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        date = request.POST.get('date')
        # Many to many field

        post_ids = request.POST.getlist('post')
        posts = Post.objects.filter(id__in=post_ids)

        comment.name = name
        comment.email = email
        comment.content = content
        comment.date = date
                                         
        comment.post.set(posts)
        comment.save()
        for post in posts:
            post.comments.add(post,)
        return redirect(reverse('view_comments'))
    else:
        return render(request, 'comment_form.html',{'comment_form':comments, 'Action':'Update'}) 



def verification_for_add_comment(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if authenticate(request, username=user_name, password=password) is not None:
            return redirect(reverse('add_comment'))
        else:
            return render(request, 'user_verification.html', {'verification_failed' : True, 'user_name':user_name, 'profile_type': 'Admin'})
    else:
        return render(request, 'user_verification.html', {'profile_type': 'Admin'})

def add_comment(request):
    comments = CommentForm()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        date = request.POST.get('date') 

        # Many to many field
        post_ids = request.POST.getlist('post')
        posts = Post.objects.filter(id__in=post_ids)
        comment=Comment(name=name, email = email, content = content, date = date)
        comment.save()
        comment.post.add(*posts)
        for post in posts:
            post.comments.add(post,)
        return redirect(reverse('view_comments'))
    else:
        return render(request, 'comment_form.html',{'comment_form':comments, 'Action':'Add'})
