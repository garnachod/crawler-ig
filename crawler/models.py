from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class SocialUser(models.Model):
    username = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64)
    photo_url = models.CharField(max_length=256)
    post_num = models.IntegerField()
    follower_num = models.IntegerField()
    following_num = models.IntegerField()
    engagement = models.FloatField(default=0.0)


class Post(models.Model):
    content = models.CharField(max_length=4096)
    img_url = models.CharField(max_length=256, unique=True)
    hashtags = models.CharField(max_length=2048)
    user = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    likes_num = models.IntegerField(default=0)
    comments_num = models.IntegerField(default=0)


@receiver(post_save, sender=Post)
def update_engagement(sender, instance, created, **kwargs):
    user = instance.user
    likes_total = 0
    comments_total = 0
    followers = user.follower_num
    post_count = 0
    for post in Post.objects.filter(user=user):
        likes_total += post.likes_num
        comments_total += post.comments_num
        post_count += 1

    user.engagement = float(likes_total + comments_total) / (float(followers) * post_count)
    user.save()
