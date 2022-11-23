from email.policy import default
from rest_framework import serializers
from .models import Laptop, Category, Rating, Like
from django.db.models import Avg

from apps.review.serializers import CommentSerializer


class LaptopSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Laptop
        fields = '__all__'

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return price

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise serializers.ValidationError('Количество не может быть отрицательным')
        return quantity

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['comments_count'] = instance.comments.all().count()
        rating = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        rep['likes'] = instance.likes.all().count()
        rep['liked_by'] = LikeSerializer(
            instance.likes.all().only('user'), many=True).data
        if rating:
            rep['rating'] = round(rating, 1)
        else:
            rep['rating'] = 0.0
        return rep


class LaptopListSerialiers(serializers.ModelSerializer):
    class Meta:
        model = Laptop
        fields = ('image', 'title', 'price', 'in_stock', 'slug')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments_count'] = instance.comment.all().count()
        return rep


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )

    class Meta:
        model = Rating
        fields = ('rating', 'user', 'laptop')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating')
        if rating not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError(
                'Wrong value! Rating must be between 1 and 5'
            )
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)


class CurrentLaptopDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['laptop']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    laptop = serializers.HiddenField(default=CurrentLaptopDefault())

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('requset').user
        laptop = self.context.get('laptop').pk
        like = Like.objects.filter(user=user, laptop=laptop).first()
        if like:
            raise serializers.ValidationError('Already liked')
        return super().create(validated_data)

    def unlike(self):
        user = self.context.get('request').user
        laptop = self.context.get('laptop').pk
        like = Like.objects.filter(user=user, laptop=laptop).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('Not liked yet')


class LikedLaptopSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='laptop.get_absolute_url')
    laptop = serializers.ReadOnlyField(source='laptop.title')

    class Meta:
        model = Like
        fields = ['laptop', 'user', 'url']