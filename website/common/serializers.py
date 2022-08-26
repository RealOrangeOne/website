from rest_framework import serializers


class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(min_value=1, default=1)
