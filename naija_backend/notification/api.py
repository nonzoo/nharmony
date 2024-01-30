from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import JsonResponse


@api_view(['GET'])
def notifications(request):
    received_notifications = request.user.received_notifications.filter(is_read=False) #get notifications that are unread
    serializer = NotificationSerializer(received_notifications, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def notification_read(request, pk):
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()

    return JsonResponse({'message':'notification read'})