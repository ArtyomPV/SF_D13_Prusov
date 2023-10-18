from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from .models import Post, Comments


class SignUp(SignupForm):

    def save(self, request):
        user = super(SignUp, self).save(request)
        # common_group = Group.objects.get(name='common')
        # common_group.user_set.add(user)
        return user


class CreatePostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'picture', 'videoLink', 'category']
        # widgets = {
        #     'title': forms.TextInput(attrs={'style': 'margin-bottom:0px'}),
        #     'text': forms.Textarea(attrs={'margin-bottom': '0px; width:100px'}),
        # }


class CreateCommentModelForm(ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'
        exclude = ['user', 'post', 'is_accepted']


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(max_length=16,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Password')
    password2 = forms.CharField(max_length=16,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Confirm Password')

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'password1': forms.PasswordInput(attrs={'class': 'form-control'}), # Для паролей виджет не работает. Чтобы задать атрибуты, например, название класса, следует использовать поле модели, как показано выше.
            # 'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return super().clean()