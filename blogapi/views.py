from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework.decorators import api_view, APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializer import *
from blogging.models import *
from .customauth import CustomAuthentication

# Create your views here.
@method_decorator(ensure_csrf_cookie,name = 'dispatch')
class GetCSRFToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'success': 'CSRF Cookie Set'
        })
    
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class TagViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Tagging.objects.all()
    serializer_class = TagSerializer

# @method_decorator(csrf_protect,name = 'dispatch')
class CommentViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        comments_data = serializer.validated_data

        # Extract post IDs from the data
        post_ids = [comment_data.pop('post', []) for comment_data in comments_data]

        # Bulk create comments
        comments_to_create = [Comment(**comment_data) for comment_data in comments_data]
        Comment.objects.bulk_create(comments_to_create)

        # Update the Many-to-Many relationship for each comment
        for comment, post_id_list in zip(comments_to_create, post_ids):
            comment.post.add(*post_id_list)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)