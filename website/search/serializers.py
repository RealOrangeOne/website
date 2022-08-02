from rest_framework import serializers

MIN_SEARCH_LENGTH = 3


class SearchParamsSerializer(serializers.Serializer):
    q = serializers.CharField(min_length=MIN_SEARCH_LENGTH)
    page = serializers.IntegerField(min_value=1, default=1)
