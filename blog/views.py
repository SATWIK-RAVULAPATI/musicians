from django.shortcuts import render,HttpResponse,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter,OrderingFilter 
from rest_framework import filters
from rest_framework import generics
from .filters import OrderFilter
from django.db.models import Q
# from rest_framework import filters

def home(request):
    #myFilter=OrderFiler(request.GEt,queryset=post)
   # Post=myFilter.qs
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)


class PostListView(ListView):
    model = Post
    template_name='blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5

class UserPostListView(ListView):
    model = Post
    template_name='blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name='posts'
    paginate_by=5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url='/'
    def test_func(self):
        post =self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post =self.get_object()
        if self.request.user == post.author:
            return True
        return False

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
  #  serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


def about(request):
    return render(request, 'blog/about.html',{'title':'About'})

def search(request):
    query = request.GET['query']
   
    allPosts1= Post.objects.filter(title__icontains=query)
    allPosts2 = Post.objects.filter(content__icontains=query)
    allPosts=allPosts1.union(allPosts2)
    
    params={'posts':allPosts,'query':query}
    return render(request,'search.html',params)

   # return HttpResponse('this is search')



