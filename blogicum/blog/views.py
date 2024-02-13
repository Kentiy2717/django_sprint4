from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone

from blog.constans import MAX_NUMBERS_POSTS_ON_PAGE
from blog.forms import ProfileForm, CommentForm, PostForm
from blog.models import Category, Comment, Post


User = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


def filtrate_posts(manager_name):
    return manager_name.select_related(
        'location',
        'author',
        'category',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = filtrate_posts(Post.objects)
    ordering = '-pub_date'
    paginate_by = MAX_NUMBERS_POSTS_ON_PAGE


class CategoryPostListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    ordering = 'title'
    paginate_by = MAX_NUMBERS_POSTS_ON_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category,
                                     slug=self.kwargs['category_slug'],
                                     is_published=True)
        context['category'] = category
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        category = get_object_or_404(Category,
                                     slug=self.kwargs['category_slug'],
                                     is_published=True)
        post_list = filtrate_posts(category.posts)
        queryset = post_list
        return queryset


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects, pk=post_id)
    if not request.user.is_anonymous:
        posts_user = request.user.posts.all()
        if post not in posts_user:
            post = get_object_or_404(filtrate_posts(Post.objects), pk=post_id)
    context = {'form': CommentForm(),
               'post': post,
               'comments': get_object_or_404(
                   Post,
                   pk=post_id).comments.order_by('created_at')}
    return render(request, 'blog/detail.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Евгений, подскажи, изначально я написал так:
        # return f'/profile/{self.request.user}/'
        # Так можно вообще или нет? Не понимаю особой разницы.
        # Ниже еще подобный пример будет в ProfileUpdateView.
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        return redirect('blog:post_detail', self.kwargs['post_id'])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    ordering = '-pub_date'
    paginate_by = MAX_NUMBERS_POSTS_ON_PAGE

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        post_list = self.user.posts.select_related('location',
                                                   'author',
                                                   'category',)
        queryset = post_list
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_success_url(self):
        # Евгений, подскажи, изначально я написал так:
        # return f'/profile/{self.request.user}/'
        # Так можно вообще или нет? Не понимаю особой разницы.
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.kwargs['username']}
        )


class AddCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

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

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.kwargs['post_id']})


class EditCommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class DeleteCommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )
