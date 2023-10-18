from allauth.account.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import PostListView, PostDetailView, CreatePostCreateView, PostUpdateView, PostDeleteView, \
    CommentPostCreateView, MyCommentsListView, CommentDeleteView, CommentDetailView, comment_accepted_send_email

app_name = 'pokorum'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/comment/', CommentPostCreateView.as_view(), name='post-comment'),
    path('create-post/', CreatePostCreateView.as_view(), name='create-post'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='edit-post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete-post'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete-comment'),
    path('comment/<int:pk>', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/', MyCommentsListView.as_view(), name='my-comments'),
    path('comment-accept/<int:pk>', comment_accepted_send_email, name='comment-accept'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
]

