from django.http import JsonResponse

from rest_framework.decorators import api_view,authentication_classes,permission_classes

from .forms import SignupForm
from .models import FriendRequest, User
from .serializers import UserSerializer,FriendRequestSerializer


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        
    })




@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'
    
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'), 
    })
    #if the form is valid the user should be saved and created
    if form.is_valid():
        form.save()
        
    else:
        message = 'error'

    return JsonResponse({'message':message})



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []
    
    if  user == request.user:
        requests = FriendRequest.objects.filter(created_for=request.user, status=FriendRequest.SENT)
        requests = FriendRequestSerializer(requests, many = True)
        requests = requests.data
    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests
    }, safe=False)


@api_view(['POST'])
def send_friend_request(request, pk):
    user = User.objects.get(pk=pk)
    check1=FriendRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2=FriendRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not check1:
        if not check2:
            friend_request = FriendRequest.objects.create(created_for=user, created_by=request.user)
            return JsonResponse({'message':'friend request created'})
    
        else:
            return JsonResponse({'message':'request already sent'})

    else:
            return JsonResponse({'message':'request already sent'})


from django.http import JsonResponse

@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friend_request = FriendRequest.objects.filter(created_for=request.user).get(created_by=user)
    
    friend_request.status = status
    friend_request.save()
    
    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()


    updated_request_data = {
        'id': friend_request.id,
        'created_by': {
            'id': friend_request.created_by.id,
            'name': friend_request.created_by.name,
            
        },
       
    }

    return JsonResponse({'message': 'friend request updated', 'updatedRequest': updated_request_data})
































