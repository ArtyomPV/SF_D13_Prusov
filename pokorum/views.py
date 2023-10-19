from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Post, User, Category, Comments
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CreatePostModelForm, CreateCommentModelForm, RegisterForm
from .filters import CommentFilter


class PostListView(ListView):
    """
    Представление показывает все объявления
    """
    template_name = 'pokorum/index.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects.all().order_by('-published_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetailView(DetailView):
    """
    Представление показывает выбранное объявление
    """
    template_name = 'pokorum/post-detail.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login'] = self.request.user
        return context


class CreatePostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление создает объявление
    """
    model = Post
    form_class = CreatePostModelForm
    template_name = 'pokorum/create-post.html'
    success_url = '/post/'
    context_object_name = 'post'

    # fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверяем, существуют ли категории,
        # и создаем дефолтные категории, если они не существуют
        if not Category.objects.count():
            create_default_categories()
        return context

    def form_valid(self, form):
        # Мы используем ModelForm, а его метод save() возвращает инстанс
        # модели, связанный с формой. Аргумент commit=False говорит о том, что
        # записывать модель в базу рановато.
        user = User.objects.get(id=self.request.user.id)
        instance = form.save(commit=False)
        instance.user_id = user.id
        instance.save()
        instance_id = str(instance.id)
        return redirect(''.join([self.success_url, instance_id]))


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление обновляет содержение объявления
    """
    form_class = CreatePostModelForm
    template_name = 'pokorum/create-post.html'
    context_object_name = 'post'
    success_url = '/'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление удаляет объявление
    """
    template_name = 'pokorum/post-delete.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    success_url = '/'


class CommentPostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление создания комментария к объявлению
    """
    model = Comments
    form_class = CreateCommentModelForm
    template_name = 'pokorum/create-comment.html'
    success_url = '/post/'
    context_object_name = 'comment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        # Мы используем ModelForm, а его метод save() возвращает инстанс
        # модели, связанный с формой. Аргумент commit=False говорит о том, что
        # записывать модель в базу рановато.
        user = User.objects.get(id=self.request.user.id)
        post = Post.objects.get(id=self.kwargs.get('pk'))
        instance = form.save(commit=False)
        instance.user_id = user.id
        instance.post_id = post.id
        instance.save()
        instance_id = str(instance.post_id)
        return redirect(''.join([self.success_url, instance_id]))


class MyCommentsListView(ListView):
    """
    Представление показывает мои отзывы
    """
    template_name = 'pokorum/show-comments.html'
    model = Comments
    context_object_name = 'comments'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CommentFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        user = self.request.user
        return Comments.objects.filter(post__user=user).order_by('-published_date')


class CommentDetailView(LoginRequiredMixin, DetailView):
    """
    Представление показывает выбранный отзыв
    """
    template_name = 'pokorum/comment-detail.html'
    model = Comments
    context_object_name = 'comment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login'] = self.request.user
        return context


class CommentDeleteView(DeleteView):
    """
    Представление удаляет отзыв
    """
    template_name = 'pokorum/comment-delete.html'
    context_object_name = 'comment'
    queryset = Comments.objects.all()
    success_url = '/comments/'


def create_default_categories():
    """
    Процедура создания категорий.
    Выполняется в случае, если список категорий пуст.
    """

    categories = ['Танки', 'Хиллы', 'DD', 'Торговцы', 'Гилдмастеры', 'Квестгиверы',
                  'Кузнецы', 'Кожевники', 'Зельевары', 'Мастеры заклинаний']
    for cat in categories:
        Category.objects.create(category=cat)


def comment_accepted_send_email(request, pk):
    comments = Comments.objects.get(pk=pk)
    comments.is_accepted = True
    comments.save()
    comment_text = comments.comment
    comment_pk = comments.pk
    post_title = comments.post.title

    email = User.objects.get(pk=comments.user.pk).email
    username = User.objects.get(pk=comments.user.pk)

    html_content = render_to_string(
        'pokorum/comment_accept.html',
        context=
        {'post_title': post_title,
         'comment_text': comment_text,
         'username': username,
         'comment_pk': comment_pk,
         'domain_url': settings.DOMAIN, }
    )

    msg = EmailMultiAlternatives(
        subject='Новый отзыв',
        from_email='django.testemail@yandex.ru',
        to=[email, ]
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return redirect('/comments/')


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'sign/register.html'
    success_url = 'login/'