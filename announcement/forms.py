from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User
from .models import Announcement, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class AnonsForm(forms.ModelForm):
    announcement = forms.CharField(widget=CKEditorUploadingWidget(), label='Объявление')

    class Meta:
        model = Announcement
        fields = ['category', 'title', 'announcement']
        widgets = {
            "announcement": CKEditorUploadingWidget(),
        }



class BasicSignupForm(SignupForm):
    """Форма дополняющая регистрационную форму allauth новыми полями.
    Необходимо прописать путь в настройкахACCOUNT_FORMS = {'signup': 'news.forms.BasicSignupForm'}"""
    email = forms.EmailField(label="Email")
    username_validator = UnicodeUsernameValidator()
    username = forms.CharField(
        label='Ник',
        max_length=150,
        validators=[username_validator],
        error_messages={
            "unique": 'Пользователь с таким именем уже зарегистрирован',
        },
    )
    first_name = forms.CharField(label='Имя', required=False)
    last_name = forms.CharField(label='Фамилия', required=False)

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


    def try_save(self, request):
        user, resp = super().try_save(request=request)
        return user, resp


    def save(self, request):
        # Автоматически добавляет всех пользователей в группу common
        user = super(BasicSignupForm, self).save(request)
        return user



