import re
from rest_framework import serializers


class YouTubeLinkValidator:
    def __init__(self, field='video_link', message='Ссылка не является видео на YouTube'):
        self.field = field
        self.message = message

    def __call__(self, value):
        video_link = value.get(self.field)
        if not video_link:
            return  # Поле video_link отсутствует или пустое, поэтому пропускаем валидацию
        youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$')
        if not youtube_pattern.match(video_link):
            raise serializers.ValidationError({self.field: [self.message]})
