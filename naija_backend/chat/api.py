from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import JsonResponse
from .models import Conversation,ConversationMessage
from .serializers import ConversationMessageSerializer,ConversationDetailSerializer,ConversationSerializer
from account.models import User

@api_view(['GET'])
def conversation_get_or_create(request, user_pk):
    user = User.objects.get(pk=user_pk)
    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user,request.user)
        conversation.save()

    serializer = ConversationDetailSerializer(conversation)

    return JsonResponse(serializer.data, safe= False)


@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))

    serializer = ConversationSerializer(conversations, many=True)

    return JsonResponse(serializer.data, safe= False)


@api_view(['GET'])
def conversation_detail(request,pk):
    conversations = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk) 
    serializer = ConversationDetailSerializer(conversations)

    return JsonResponse(serializer.data, safe= False)


@api_view(['POST'])
def conversation_send_message(request,pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk) 

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user


    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to
    )

    serializer = ConversationMessageSerializer(conversation_message)

    return JsonResponse(serializer.data, safe= False)