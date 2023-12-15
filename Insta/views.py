#from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from Insta.models import Post, Like, InstaUser, UserConnection

from Insta.forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from annoying.decorators import ajax_request



#HelloWorld is-a TemplateView

class HelloWorld(TemplateView): 
    template_name = 'test.html'

#ListView 会把所有的model作为list of objects返回出来，叫做object_list，并传递给template_name
class PostsView(ListView):
    model = Post
    template_name = 'index.html'

    def get_queryset(self):
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following) 

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    #CreateView里有一个field，可以让用户提供基于model的信息，比如这里，即可以让用户提供post的image，title等
    fields = '__all__' #django语法，即提供所有关于post的信息, 但不包含自动生成的部分，在这里即不包含id
    login_url = 'login'

class PostUpdateView(UpdateView): 
    model = Post
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    #因为不能在执行删除的同时进行跳转，所以在进行删除操作的时候要用reverse_lazy
    success_url = reverse_lazy("posts")
 
class Signup(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")

class UserDetailView(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'


@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1 
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }