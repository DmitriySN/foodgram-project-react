from api.paginators import CustomPagination
from api.serializers import CustomUserSerializer, SubscribeSerializer
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Subscribe, User


class UserViewSet(UserViewSet):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = CustomUserSerializer

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
            if Subscribe.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                Subscribe.objects.create(user=user, author=author)
                follow = Subscribe.objects.get(user=user, author=author)
                serializer = SubscribeSerializer(follow)
                return Response(
                    data=serializer.data, status=status.HTTP_201_CREATED
                )

        if request.method == 'DELETE':
            follow = Subscribe.objects.filter(user=user, author=author)
            if follow.exists():
                follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['GET'],
        permission_classes=[IsAuthenticated],
        pagination_class=CustomPagination
    )
    def subscriptions(self, request):
        user = request.user
        following = Subscribe.objects.filter(user=user)
        pagination = self.paginate_queryset(following)
        serializer = SubscribeSerializer(pagination, many=True)
        return self.get_paginated_response(serializer.data)
