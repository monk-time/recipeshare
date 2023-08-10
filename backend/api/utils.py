from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError


def generate_action(
    model,
    serializer_class,
    url: str,
    m2m_field_name: str,
    error_texts: dict[str, str],
):
    """Создать эндпоинт для пары действий POST/DELETE для M2M-полей."""

    def action_func(self, request, pk):
        user = request.user
        instance = get_object_or_404(model, pk=pk)
        m2m_field = getattr(instance, m2m_field_name)

        if request.method == 'POST':
            if m2m_field.contains(user):
                raise ValidationError(error_texts['POST'])
            m2m_field.add(user)
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not m2m_field.contains(user):
                raise ValidationError(error_texts['DELETE'])
            m2m_field.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    action_func.__name__ = url
    return action(
        methods=['post', 'delete'],
        detail=True,
        serializer_class=serializer_class,
        url_path=url,
    )(action_func)
