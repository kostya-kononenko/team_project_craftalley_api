from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _

from user.models import Rating


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "image",
            "about_myself",
            "date_of_birth",
            "brand_name",

        )
        read_only_fields = ("id", "is_stuff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserDetailSerializer(UserSerializer):
    middle_star = serializers.IntegerField(read_only=True)
    rating_user = serializers.BooleanField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "about_myself",
            "image",
            "date_of_birth",
            "brand_name",
            "middle_star",
            "rating_user",
        )


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = _("User account is disabled.")
                    raise serializers.ValidationError(msg,
                                                      code="authorization")
            else:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg,
                                                  code="authorization")
        else:
            msg = _("Must include 'username' and 'password'.")
            raise serializers.ValidationError(msg,
                                              code="authorization")

        attrs["user"] = user
        return attrs


class CreateUserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("star", "user", "ip")

        def create(self, validate_data):
            rating = Rating.objects.update_or_create(
                ip=validate_data.get("ip", None),
                user=validate_data.get("user", None),
                defaults={"star": validate_data.get("star")},
            )
            return rating
