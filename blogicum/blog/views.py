from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.constants import NUMBER_OF_POSTS_ON_USER_PAGE
from blog.forms import CommentForm, PostForm, ProfileForm
from blog.mixins import (CommentModelMixin, OnlyAuthorMixin, PostModelMixin,
                         ReturnToPostMixin, ReturnToProfileMixin,
                         UserModelMixin)
from blog.models import Category, Post
from blog.utils import count_and_order

User = get_user_model()


class PostCreateView(
    LoginRequiredMixin,
    PostModelMixin,
    ReturnToProfileMixin,
    CreateView
):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    PostModelMixin,
    UpdateView
):

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail',
            post_id=self.kwargs['post_id']
        )


class PostDeleteView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    PostModelMixin,
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
        return count_and_order()


class PostDetailView(PostModelMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_object(self):
        post = super().get_object()
        if post.author != self.request.user:
            return get_object_or_404(Post.published, id=self.kwargs['post_id'])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (self.object.comments.select_related('author'))
        return context


class CommentCreateView(
    LoginRequiredMixin,
    CommentModelMixin,
    ReturnToPostMixin,
    CreateView
):

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    CommentModelMixin,
    ReturnToPostMixin,
    UpdateView
):
    pass


class CommentDeleteView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    CommentModelMixin,
    ReturnToPostMixin,
    DeleteView
):
    pass


class ProfileListView(UserModelMixin, ListView):
    template_name = 'blog/profile.html'
    paginate_by = NUMBER_OF_POSTS_ON_USER_PAGE

    def get_queryset(self):
        user = get_object_or_404(
            User, username=self.kwargs['username'])
        if user != self.request.user:
            return count_and_order().filter(
                author=user
            )
        return Post.objects.annotate(
            comment_count=Count('comments')
        ).filter(
            author=user
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(
            User, username=self.kwargs['username'])
        context['profile'] = user
        return context


class ProfileUpdateView(LoginRequiredMixin, UserModelMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            args=[self.object.username]
        )


class CategoryListlView(ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = NUMBER_OF_POSTS_ON_USER_PAGE

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category'],
            is_published=True
        )
        return count_and_order().filter(
            category=category
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        select_category = get_object_or_404(
            Category,
            slug=self.kwargs['category'],
            is_published=True
        )
        context['category'] = select_category
        return context
