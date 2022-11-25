# api/views.py

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Post, Comment
from . import serializers

@api_view(['GET'])
def index(request):
    return Response()

class PostListView(generics.ListAPIView):
    """
    Returns a list of published posts
    """
    serializer_class = serializers.PostListSerializer
    queryset = Post.objects.published()

class PostDetailView(generics.RetrieveAPIView):
    """
    Returns post details
    """
    serializer_class = serializers.PostDetailSerializer
    queryset = Post.objects.published()

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all().order_by('-created')

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        queryset = super().get_queryset()
        if post_id and post_id.isdecimal():
            queryset = queryset.filter(post_id=int(post_id))

        return queryset.order_by('-created')
