from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from django.urls import reverse

# Create your models here.

class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        #图片上传到后端的什么位置
        upload_to = 'static/images/profiles',
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True
        )
        
    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    #看是否被当前user follow
    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()


class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username

class Post(models.Model):
    author = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name = 'my_posts'
    )
    title = models.TextField(blank = True, null = True)
    # image = models.ImageField function is not enough
    image = ProcessedImageField(
        #图片上传到后端的什么位置
        upload_to = 'static/images/posts',
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True
        )

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])

    def get_like_count(self):
        return self.likes.count()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'likes')
    user = models.ForeignKey(InstaUser, on_delete = models.CASCADE, related_name = 'likes')
    class Meta:
         unique_together = ("post", "user")  # meaning this pair is unique

    def __str__(self):
        return 'Likes: ' + self.user.username + ' likes ' + self.post.title
    
