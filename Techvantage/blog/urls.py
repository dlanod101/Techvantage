from django.urls import path
from .views import CreateBlogPostView

urlpatterns = [
    path('blog/', CreateBlogPostView.as_view(), name='blog_create')
]

