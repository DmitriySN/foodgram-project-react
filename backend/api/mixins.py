from rest_framework import mixins, viewsets


class CreateUpdateRetrieveViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    ...
