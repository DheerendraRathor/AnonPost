__author__ = 'dheerendra'

from rest_framework import serializers
from models import Post, Reply
from django.conf import settings


class ReplySerializer(serializers.ModelSerializer):

    user_type = serializers.SerializerMethodField()

    def get_user_type(self, reply):
        username = reply.user.username
        if username in settings.ADMIN_USERNAMES:
            return 'A'
            # Admin User
        else:
            return 'N'
            # Normal User

    class Meta:
        model = Reply
        fields = ('id', 'message', 'user_type')


class PostSerializer(serializers.ModelSerializer):

    reply_count = serializers.IntegerField(source='replies.count')

    class Meta:
        model = Post
        fields = ('id', 'title', 'message', 'reply_count')
