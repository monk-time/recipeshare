from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser import views
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api.serializers import UserFollowSerializer
from users.models import Follow

User = get_user_model()


class UserViewSet(views.UserViewSet):
    http_method_names = ['get', 'post', 'delete']

    def destroy(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    @action(detail=False, serializer_class=UserFollowSerializer)
    def subscriptions(self, request):
        followed_users = User.objects.filter(
            following__follower=self.request.user
        )

        page = self.paginate_queryset(followed_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(followed_users, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['post'],
        serializer_class=UserFollowSerializer,
    )
    def subscribe(self, request, id):
        follower = request.user
        following = get_object_or_404(User, pk=id)

        if Follow.objects.filter(
            follower=follower, following=following
        ).exists():
            raise ValidationError('Эта подписка уже существует.')
        if follower == following:
            raise ValidationError('Нельзя подписаться на самого себя.')

        Follow.objects.create(follower=follower, following=following)

        serializer = self.get_serializer(following)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id):
        follow = Follow.objects.filter(
            follower=request.user,
            following=get_object_or_404(User, pk=id),
        )
        if not follow.exists():
            raise ValidationError('Подписки не существует.')
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
