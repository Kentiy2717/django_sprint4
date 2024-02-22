from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse

from blog.constans import MAX_NUMBERS_POSTS_ON_PAGE
from blog.forms import ProfileForm, CommentForm, PostForm
from blog.models import Category, Post, User
from blog.mixins import CommentMixin, CommentUrlKwargMixin, PostMixin
from blog.services import comment_count, filtrate_posts


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = comment_count(filtrate_posts(Post.objects))
    paginate_by = MAX_NUMBERS_POSTS_ON_PAGE


class CategoryPostListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    ordering = 'title'
    paginate_by = MAX_NUMBERS_POSTS_ON_PAGE

    def get_category(self):
        return get_object_or_404(Category,
                                 slug=self.kwargs['category_slug'],
                                 is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        post_list = comment_count(filtrate_posts(self.get_category().posts))
        queryset = post_list
        return queryset


class PostDetailView(ListView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    paginate_by = MAX_NUMBERS_POSTS_ON_PAGE

    def get_queryset(self):
        return self.get_object().comments.all()

    def get_object(self):
        obj = get_object_or_404(Post.objects,
                                pk=self.kwargs[self.pk_url_kwarg],)
        if obj.author == self.request.user:
            return obj
        return get_object_or_404(filtrate_posts(Post.objects),
                                 pk=self.kwargs[self.pk_url_kwarg],)

    def get_context_data(self, **kwargs):
        self.context_object_name = 'post'
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['post'] = self.get_object()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostUpdateView(PostMixin, UpdateView):

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(PostMixin, DeleteView):
    pass


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = MAX_NUMBERS_POSTS_ON_PAGE

    def get_profile(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        author = self.get_profile()
        queryset = comment_count(author.posts)
        if author != self.request.user:
            return filtrate_posts(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.kwargs['username']}
        )


class AddCommentCreateView(CommentMixin, CreateView):

    def dispatch(self, request, *args, **kwargs):
        self.blog_post = get_object_or_404(
            Post,
            pk=kwargs['post_id']
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)


class EditCommentUpdateView(CommentUrlKwargMixin, UpdateView):
    pass


class DeleteCommentDeleteView(CommentUrlKwargMixin, DeleteView):
    pass
