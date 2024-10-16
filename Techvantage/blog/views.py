from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from utilities.authentication import FirebaseAuthentication
from .models import BlogPost  # Assuming a BlogPost model exists

class CreateBlogPostView(APIView):
    permission_classes = [IsAuthenticated]  # User must be authenticated
    authentication_classes = [FirebaseAuthentication]

    def post(self, request, *args, **kwargs):
        # Access the current authenticated user
        user = request.user

        # Get the data from the request
        title = request.data.get('title')
        content = request.data.get('content')

        # Create a new blog post with the authenticated user as the author
        post = BlogPost.objects.create(author=user, title=title, content=content)

        return Response({
            'user': user.display_name,
            'message': 'Post created successfully',
            'post_id': post.id
        }, status=status.HTTP_201_CREATED)
