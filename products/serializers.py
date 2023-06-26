from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'title', 'brand', 'selling_price', 'offering_price', 'image', 'description', 'slug', 'created_at',
            'updated_at')
