from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse

from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post

User = get_user_model()


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
            args=[self.request.user]
        )


class ReturnToPostMixin:

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            args=[self.object.post_id]
        )
