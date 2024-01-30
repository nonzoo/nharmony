from .models import Notification
from post.models import Post
from account.models import FriendRequest

def create_notification(request,type_of_notification, post_id=None,friendrequest_id=None):
    created_for = None
    if type_of_notification == 'post_like':
        body = f"{request.user.name} liked your post"
        post = Post.objects.get(pk=post_id)
        created_for= post.created_by

    elif type_of_notification == 'post_comment':
        body = f"{request.user.name} commented on your post"
        post = Post.objects.get(pk=post_id)
        created_for= post.created_by

    elif type_of_notification == 'new_friendrequest':
        friendrequest = FriendRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f"{request.user.name} sent you a friend request"


    elif type_of_notification == 'accepted_friendrequest':
        friendrequest = FriendRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_by
        body = f"{request.user.name} accepted your friend request"


    elif type_of_notification == 'rejected_friendrequest':
        friendrequest = FriendRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f"{request.user.name} rejected your friend request"





    notification = Notification.objects.create(
        body=body,
        created_by=request.user,
        type_of_notification=type_of_notification,
        post_id=post_id,
        created_for=created_for
    )

    return notification