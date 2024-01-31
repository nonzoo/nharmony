from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import JsonResponse
from .models import Post, Like, Comment,Trend
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer,TrendSerializer
from .forms import PostForm,AttachmentsForm
from account.models import User
from account.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from notification.utils import create_notification


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]
    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    trend = request.GET.get('trend', '')
 
    if trend:
        posts = posts.filter(body__icontains='#' + trend)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    serializer = PostDetailSerializer(post)
    return JsonResponse({
        'post':serializer.data
    })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    
    context = {'posts': post_serializer.data, 'user': user_serializer.data}
    return JsonResponse(context,safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment=None
    attachment_form = AttachmentsForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        
        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=True)
    else:
        return JsonResponse({'error': 'Invalid form data'}, status=400)



@require_POST
@api_view(['POST'])
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    if post.likes.filter(created_by=user).exists():
        # If the user already liked the post, remove the like
        like = post.likes.get(created_by=user)
        like.delete()
        post.likes_count -= 1
        post.save()


        return JsonResponse({'message': 'like removed', 'likes_count': post.likes_count})
    else:
        # If the user has not liked the post, add the like
        like = Like.objects.create(created_by=user,created_for=post.created_by)
        post.likes.add(like)
        post.likes_count += 1
        post.save()
        notification = create_notification(request, 'post_like' , post_id=post.id)
        return JsonResponse({'message': 'like created', 'likes_count': post.likes_count})


@api_view(['POST'])
def post_create_comment(request ,pk):
    post = Post.objects.get(pk=pk)
    comment = Comment.objects.create(
        body = request.data.get('body'),
        created_by = request.user,
        created_for = post.created_by,
        commented_on = post,
        )
    
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    serializer = CommentSerializer(comment)

    notification = create_notification(request, 'post_comment' , post_id=post.id)

    return JsonResponse(serializer.data, safe=False)




@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_trends(request):
    trends = Trend.objects.all()

    serializer = TrendSerializer(trends, many = True)

    return JsonResponse(serializer.data, safe=False)