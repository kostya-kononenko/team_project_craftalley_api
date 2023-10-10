from rest_framework import serializers

from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "date_posted",
            "product",
        )


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "date_posted",
            "product",
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")

    class Meta:
        model = Comment
        fields = (
            "content",
            "date_posted",
            "first_name",
            "last_name"
        )


class CommentImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=False)

    class Meta:
        model = Comment
        fields = ("id", "image")
