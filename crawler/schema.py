import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import SocialUser, Post
import django_filters
from graphene import relay


class SocialUserType(DjangoObjectType):
    class Meta:
        model = SocialUser
        filter_fields = {
            'username': ['icontains'],
            'post_num': ['lt', 'gt'],
            'follower_num': ['lt', 'gt'],
            'following_num': ['lt', 'gt'],
            'engagement': ['lt', 'gt'],
            'hashtags': ['icontains']}
        interfaces = (relay.Node,)

class SocialUserFilter(django_filters.FilterSet):
    hashtags = django_filters.CharFilter(name="hashtags", method='my_hashtags_filter')

    class Meta:
        model = SocialUser
        fields = {
            'username': ['icontains'],
            'post_num': ['lt', 'gt'],
            'follower_num': ['lt', 'gt'],
            'following_num': ['lt', 'gt'],
            'engagement': ['lt', 'gt'],
            'hashtags': ['icontains']
        }

    def my_hashtags_filter(self, queryset, name, value):
        ids_accepted = []
        for socialuser in queryset:
            if Post.objects.filter(user=socialuser, hashtags__icontains=value).count() > 0:
                ids_accepted.append(socialuser.id)
        return queryset.filter(pk__in=ids_accepted)


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = {'content': ['icontains']}
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    social_user = relay.Node.Field(SocialUserType)
    all_social_users = DjangoFilterConnectionField(SocialUserType, filterset_class=SocialUserFilter)
    all_posts = DjangoFilterConnectionField(PostType)

    def resolve_all_social_users(self, info, **kwargs):
        return SocialUser.objects.all()

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()


schema = graphene.Schema(query=Query)