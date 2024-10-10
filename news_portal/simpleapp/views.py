from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.views import View


# News List View
class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(type='NW')  # Filter for news posts
    paginate_by = 10  # Number of posts per page

# News Detail View
class NewsDetailView(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'

# News Create View
class NewsCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'  # Set post type to News
        post.save()
        return super().form_valid(form)

# News Update View
class NewsUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'  # Ensure the type remains News
        post.save()
        return super().form_valid(form)

# News Delete View
class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type='NW')  # Only delete News posts

# Article Create View
class ArticleCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'  # Set post type to Article
        post.save()
        return super().form_valid(form)

# Article Update View
class ArticleUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'  # Ensure the type remains Article
        post.save()
        return super().form_valid(form)

# Article Delete View
class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'article_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type='AR')  # Only delete Article posts

# Search View
class SearchView(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        author_name = self.request.GET.get('author')
        after_date = self.request.GET.get('date_after')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author_name:
            queryset = queryset.filter(author__user__username__icontains=author_name)
        if after_date:
            queryset = queryset.filter(created_at__date__gt=after_date)

        return queryset

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class MyView(PermissionRequiredMixin, View):
    permission_required = ('simpleapp.add_post', 'simpleapp.change_post')

