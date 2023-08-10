from django.contrib.auth import get_user_model
from djoser import serializers as djoser_serializers
from rest_framework import serializers

from users.models import Follow

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
            and Follow.objects.filter(
                follower=current_user, following=obj
            ).exists()
        )
