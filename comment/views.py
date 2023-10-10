from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from comment.models import Comment
from comment.permissions import IsOwnerOrReadOnly

from comment.serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    CommentImageSerializer,
    CommentListSerializer,
)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer
        if self.action == "retrieve":
            return CommentDetailSerializer
        if self.action == "create":
            return CommentSerializer
        if self.action == "upload_image":
            return CommentImageSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["POST"],
        url_path="upload_image",
        permission_classes=(IsOwnerOrReadOnly,),
    )
    def upload_image(self, request, pk=None):
        comment = self.get_object()
        serializer = self.get_serializer(comment, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
