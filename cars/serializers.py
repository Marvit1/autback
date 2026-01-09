from rest_framework import serializers
from .models import Car, CarImage, CarTranslation

class CarImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = CarImage
        fields = ['id', 'image']
        read_only_fields = ['id']

class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'make', 'model', 'year', 'price', 
            'mileage', 'color', 'fuel', 'transmission', 
            'description', 'created_at', 'images', 'status',
        ]
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        lang = None
        if request:
            # prefer explicit ?lang=xx then Accept-Language header short code
            lang = request.query_params.get('lang') or (request.headers.get('Accept-Language', '')[:2] if request.headers.get('Accept-Language') else None)
        lang = (lang or 'hy') if isinstance(lang, str) else 'hy'

        def _normalize_field(val, lang_code):
            # If value comes as an object with localized keys or structured content,
            # pick the best text for the requested language.
            if val is None:
                return ''
            if isinstance(val, dict):
                # prefer exact lang code first
                if lang_code in val and isinstance(val[lang_code], str):
                    return val[lang_code]
                # common fields
                for k in ('text', 'content', 'html', 'name', 'label', 'title', 'value'):
                    if k in val and isinstance(val[k], str):
                        return val[k]
                # fallback to first string entry
                for v in val.values():
                    if isinstance(v, str):
                        return v
                return ''
            return val

        translation = instance.get_translation(lang)
        if translation:
            data['make'] = translation.make
            data['model'] = translation.model
            data['description'] = translation.description

        # Ensure fields that may be objects are normalized into plain strings
        for key in ('fuel', 'transmission', 'color', 'description'):
            if key in data:
                data[key] = _normalize_field(data.get(key), lang)

        # include the language used in the response for debugging/client usage
        data['_locale'] = lang
        return data