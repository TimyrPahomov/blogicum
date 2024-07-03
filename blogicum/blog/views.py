from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.forms import CommentForm, PostForm, UserUpdateForm
from blog.models import Category, Comment, Post

User = get_user_model()

NUMBER_OF_POSTS_ON_USER_PAGE = 10


class PostModelMixin:
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'


class CommentModelMixin:
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'


class UserModelMixin:
    model = User


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class ReturnToProfileMixin:

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class PostCreateView(
    PostModelMixin,
    LoginRequiredMixin,
    ReturnToProfileMixin,
    CreateView
):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    PostModelMixin,
    OnlyAuthorMixin,
    UpdateView
):

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail',
            post_id=self.kwargs['post_id']
        )


class PostDeleteView(
    PostModelMixin,
    OnlyAuthorMixin,
    ReturnToProfileMixin,
    DeleteView
):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context


class PostListView(PostModelMixin, ListView):
    template_name = 'blog/index.html'
    paginate_by = NUMBER_OF_POSTS_ON_USER_PAGE

    def get_queryset(self):
        return Post.published.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')


class PostDetailView(PostModelMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        if post.author != self.request.user:
            return Post.published.all()
        else:
            return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (self.object.comments.select_related('author'))
        return context


class CommentCreateView(
    CommentModelMixin,
    LoginRequiredMixin,
    CreateView
):
    publication = None

    def dispatch(self, request, *args, **kwargs):
        self.publication = get_object_or_404(Post, id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.publication
        return super().form_valid(form)


class CommentUpdateView(
    CommentModelMixin,
    OnlyAuthorMixin,
    UpdateView
):
    pass


class CommentDeleteView(
    CommentModelMixin,
    OnlyAuthorMixin,
    DeleteView
):

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post_id}
        )


class ProfileListView(UserModelMixin, ListView):
    template_name = 'blog/profile.html'
    paginate_by = NUMBER_OF_POSTS_ON_USER_PAGE

    def get_queryset(self):
        if self.kwargs['username'] != self.request.user.username:
            return Post.published.annotate(
                comment_count=Count('comments')
            ).filter(
                author__username=self.kwargs['username']
            ).order_by('-pub_date')
        else:
            return Post.objects.annotate(
                comment_count=Count('comments')
            ).filter(
                author__username=self.kwargs['username']
            ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(
            User, username=self.kwargs['username'])
        context['profile'] = user
        return context


class ProfileUpdateView(UserModelMixin, LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.username}
        )


class CategoryListlView(ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = NUMBER_OF_POSTS_ON_USER_PAGE

    def get_queryset(self):
        return Post.published.annotate(
            comment_count=Count('comments')
        ).filter(
            category__slug=self.kwargs['category']
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        select_category = get_object_or_404(
            Category,
            slug=self.kwargs['category'],
            is_published=True
        )
        context['category'] = select_category
        return context
