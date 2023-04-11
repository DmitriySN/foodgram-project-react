from http import HTTPStatus

from django.contrib.auth import get_user_model
from api.paginators import CustomPagination
from api.serializers import CustomUserSerializer, SubscribeSerializer
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Subscribe

User = get_user_model()


class UsersViewSet(UserViewSet):
    queryset = Subscribe.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = CustomUserSerializer

    @action(
        detail=False, methods=['GET'],
        permission_classes=[IsAuthenticated],
        pagination_class=CustomPagination
    )
    def subscriptions(self, request):
        following = User.objects.filter(
            following__user=request.user).order_by('pk')
        recipes_limit = self.request.query_params.get('recipes_limit')
        pagination = self.paginate_queryset(following)
        serializer = SubscribeSerializer(
            pagination, many=True,
            context={'request': request, 'recipes_limit': recipes_limit}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True, methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)
        if user == author:
            return Response(
                {'errors': 'Подписаться на себя нельзя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'POST':
            obj, created = Subscribe.objects.get_or_create(
                user=user, author=author
            )
            if created:
                return Response(HTTPStatus.CREATED)
            return Response(
                {'errors': 'Вы уже подписаны'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'DELETE':
            follow = Subscribe.objects.filter(user=user, author=author)
            if follow.exists():
                follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
