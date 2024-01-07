from .models import Post, PostAttachment
from django.forms import ModelForm


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields  = ('body', )

class AttachmentsForm(ModelForm):

    class Meta:
      model = PostAttachment
      fields = ('image', )