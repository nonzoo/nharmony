from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import JsonResponse
from account.models import User
from account.serializers import UserSerializer
from post.serializers import PostSerializer
from post.models import Post
from django.db.models import Q


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def search(request):
    data = request.data  
    query = data['query']

    users = User.objects.filter(Q(name__icontains=query) | Q(locations__icontains=query) )
    users_serializer = UserSerializer(users, many=True)

    posts= Post.objects.filter(body__icontains=query)
    post_serializer = PostSerializer(posts, many= True)

    context={
        'users':users_serializer.data,
        'posts':post_serializer.data,
        
    }
    return JsonResponse(context, safe = False) 

"""Q(bio__icontains=query) |"""