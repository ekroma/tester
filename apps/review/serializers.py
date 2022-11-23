from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs