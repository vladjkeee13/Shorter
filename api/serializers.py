import random
import string

from rest_framework import serializers
from core.models import Url
from core.tasks import parse_original_url


class UrlSerializer(serializers.ModelSerializer):

    author = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    expiration_date = serializers.DateTimeField(read_only=True)
    clicks = serializers.IntegerField(read_only=True, default=0)
    text = serializers.CharField(read_only=True)

    class Meta:
        model = Url
        fields = '__all__'

    def create(self, validated_data):

        url = super(UrlSerializer, self).create(validated_data)
        try:
            url.author = self.context['request'].user
        except:
            pass

        if not validated_data['short_url']:
            short_url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            url.short_url = short_url

        url.save()

        parse_original_url.delay(url.id)

        return url
