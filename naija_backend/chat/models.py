from django.db import models
import uuid
from django.contrib.auth import get_user_model
from account.models import User
from account.time import created_at_format
from django.utils import timezone
# User = get_user_model()


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)
                    
    
    def modified_at_formatted(self):
        return created_at_format(self.modified_at)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super(Conversation, self).save(*args, **kwargs)




class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def created_at_formatted(self):
        return created_at_format(self.created_at)
    
    # def __str__(self):
    #     return(f"From {self.created_by.name} to {self.sent_to.name}--{self.body[:10]}")

    def save(self, *args, **kwargs):
        super(ConversationMessage, self).save(*args, **kwargs)
        # Update the modified_at field in the associated Conversation model
        self.conversation.modified_at = timezone.now()
        self.conversation.save()
    