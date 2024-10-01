from rest_framework import serializers
from apps.cats.models import Breeds, Cats, CatRating
from datetime import datetime
from django.db.models import Avg


class BreedsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Breeds
        fields = "__all__"


class CatsSerializers(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Cats
        fields = "__all__"

    ''' возраст (полных месяцев) '''

    def get_month(self, obj):
        if obj.age:
            now = datetime.now()
            months = (now.year - obj.age.year) * 12 + now.month - obj.age.month
            return months
        return None

    def get_average_rating(self, obj):
        return obj.catrating_set.aggregate(Avg('rating'))['rating__avg'] or 0

    def create(self, validated_data):
        instance = Cats.objects.create(**validated_data)
        return instance


class CatRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatRating
        fields = ['cat', 'rating']
