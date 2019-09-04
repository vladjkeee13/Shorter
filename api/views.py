from rest_framework.viewsets import ModelViewSet

from api.serializers import UrlSerializer
from core.models import Url


class APIUrls(ModelViewSet):

    queryset = Url.objects.all().order_by('-id')
    serializer_class = UrlSerializer

