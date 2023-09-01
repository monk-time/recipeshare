from django.conf import settings
from django.contrib.auth import get_user_model
from djoser import serializers as djoser_serializers
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        read_only_fields = ('id',)

    def validate_password(self, password):
        if len(password) > settings.MAX_LENGTH_PASSWORD:
            raise serializers.ValidationError(
                'Пароль должен иметь не более '
                f'{settings.MAX_LENGTH_PASSWORD} символов.'
            )
        return password


class UserSerializer(djoser_serializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user  # type: ignore
        return (
            current_user.is_authenticated
            and obj.following.filter(follower=current_user).exists()
        )
