from django.db import models
import uuid
from django.contrib.auth import get_user_model
from account.time import created_at_format
User = get_user_model()




class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE) # the user that commented
    commented_on = models.ForeignKey('Post', related_name='post_comments', null=True, on_delete=models.CASCADE) #the post that was commented on
    created_for = models.ForeignKey(User, related_name='comment_for', null=True, on_delete=models.CASCADE) # the user that got the comment
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def created_at_formatted(self):
        return created_at_format(self.created_at)
        
    def __str__(self): #I added a check using 'hasattr' to ensure that 'self.created_by' and 'self.created_for' have the attribute 'name' before trying to access it.
        created_by_name = self.created_by.name if self.created_by and hasattr(self.created_by, 'name') else "Unknown User"
        created_for_name = self.created_for.name if self.created_for and hasattr(self.created_for, 'name') else "Unknown User"
        return f"{created_by_name} commented on {created_for_name}'s post, {self.commented_on}"




class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #image = models.ImageField(upload_to= f'post_attachments/{User.email}')
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)




class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post_liked = models.ForeignKey('Post', related_name='post_like', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_for = models.ForeignKey(User, related_name='liked_by', null=True ,on_delete=models.CASCADE)

    
    class Meta:
        ordering = ('-created_at',)




class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)

    attachments = models.ManyToManyField(PostAttachment, blank=True)

    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)  # validators=[validate_non_negative]

    comments = models.ManyToManyField(Comment, related_name='comments_for_post', blank=True)
    comments_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    def created_at_formatted(self):
        return created_at_format(self.created_at)

    def __str__(self):
        return self.body[:20]
    