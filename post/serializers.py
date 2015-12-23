import html5lib
from html5lib import sanitizer, treewalkers, serializer
from rest_framework import serializers

from models import Post, Reply


class ReplySerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    def get_user_type(self, reply):
        original_poster = reply.post.user
        if reply.user == original_poster:
            return 'N'
        else:
            return 'A'

    class Meta:
        model = Reply
        fields = ('id', 'message', 'user_type')


class PostSerializer(serializers.ModelSerializer):
    reply_count = serializers.IntegerField(source='replies.count')

    class Meta:
        model = Post
        fields = ('id', 'title', 'message', 'reply_count')


def sanitize_html(html):
    tree = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer).parseFragment(html)
    walker = treewalkers.getTreeWalker('etree')
    stream = walker(tree)
    return serializer.HTMLSerializer(quote_attr_values=True,
                                     alphabetical_attributes=True,
                                     omit_optional_tags=False).render(stream)
