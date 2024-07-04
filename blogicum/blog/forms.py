from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post

User = get_user_model()


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        label='Имя',
        help_text=(
            'Введите ваше имя. '
            'Не более 50 символов. '
        )
    )
    last_name = forms.CharField(
        max_length=50,
        label='Фамилия',
        required=False,
        help_text=(
            'Введите вашу фамилию. '
            'Не более 50 символов. '
            'Небязательное поле.'
        )
    )
    email = forms.EmailField(
        help_text='Введите адрес вашей электронной почты. '
    )
    username = forms.SlugField(
        max_length=50,
        label='Имя пользователя',
        help_text=(
            'Уникальное имя под которым вас будут видеть другие пользователи. '
            'Не более 50 символов. '
            'Только буквы, цифры и символы -/_.'
        )
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class ProfileCreationForm(ProfileForm, UserCreationForm):
    pass


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'pub_date',
            'image',
            'location',
            'category',
            'is_published'
        )
        widgets = {
            'pub_date': forms.widgets.DateTimeInput(
                attrs={'type': 'datetime-local'}
            )
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['cols'] = 10
        self.fields['text'].widget.attrs['rows'] = 5
