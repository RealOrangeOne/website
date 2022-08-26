from rest_framework import serializers

from website.common.serializers import PaginationSerializer

MIN_SEARCH_LENGTH = 3


class SearchParamsSerializer(PaginationSerializer):
    q = serializers.CharField(min_length=MIN_SEARCH_LENGTH)
