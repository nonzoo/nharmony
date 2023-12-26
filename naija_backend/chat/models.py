from django.db import models
import uuid
from account.models import User
from account.time import created_at_format
from django.utils import timezone

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def modified_at_formatted(self):
        return created_at_format(self.modified_at)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super(Conversation, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-modified_at',)


class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def created_at_formatted(self):
        return created_at_format(self.created_at)

    def save(self, *args, **kwargs):
        super(ConversationMessage, self).save(*args, **kwargs)
        # Update the modified_at field in the associated Conversation model
        self.conversation.modified_at = timezone.now()
        self.conversation.save()
