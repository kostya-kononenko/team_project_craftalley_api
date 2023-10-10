from rest_framework import serializers

from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "image",
            "user",
            "date_posted",
            "product",
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")

    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "image",
            "user",
            "date_posted",
            "product",
        )
