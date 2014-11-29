from rest_framework import serializers

from .models import Wallpaper

class WallpaperSerializer(serializers.ModelSerializer):
    # Altered fields
    image = serializers.URLField(source='image.url', read_only=True)

    # Virtual fields
    repr = serializers.CharField(source='__str__', read_only=True)
    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)
    download_url = serializers.URLField(source='get_download_url', read_only=True)
    full_search_url = serializers.URLField(source='get_full_search_url', read_only=True)
    tags = serializers.SerializerMethodField('get_tags')

    class Meta:
        model = Wallpaper
        fields = (
            # Natural fields
            'id', 'name', 'image', 'height', 'width', 'raw_ratio', 'fractional_ratio', 'uploader',
            'author', 'license', 'duplicate_of', 'date_created', 'is_public', 'purity_rating',
            'views',

            # Virtual fields
            'repr', 'absolute_url', 'download_url', 'full_search_url', 'tags',
        )

    def get_tags(self, obj):
        return obj.tags.all()
