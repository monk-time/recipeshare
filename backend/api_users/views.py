from django.contrib.auth import get_user_model
from django.db.models import Count
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserFollowSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    http_method_names = ['get', 'post', 'delete']

    def destroy(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    @action(detail=False, serializer_class=UserFollowSerializer)
    def subscriptions(self, request):
        followed_users = (
            User.objects.filter(following__follower=self.request.user)
            .annotate(recipes_count=Count('recipes'))
            .order_by('id')
        )

        page = self.paginate_queryset(followed_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(followed_users, many=True)
        return Response(serializer.data)
