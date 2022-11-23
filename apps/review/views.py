from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .serializers import CommentSerializer
from .models import Comment


class CommentView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

        