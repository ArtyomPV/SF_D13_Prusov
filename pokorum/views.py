from django.views.generic import ListView, DetailView
from .models import Post


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
