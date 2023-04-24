from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class DynamicFieldsMixin:
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CustomCategorySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CustomProductSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    category = CustomCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        context = self.context.copy()
        category_fields = context.get('category_fields', [])
        option_fields = context.get('option_fields', [])

        if category_fields != []:
            self.fields['category'] = CustomCategorySerializer(read_only=True, fields=category_fields)
        if option_fields != []:
            self.fields['option'] = CustomCategorySerializer(read_only=True, fields=option_fields)
        return super().to_representation(instance)


class CustomOrderSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    product = CustomProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        context = self.context.copy()
        product_fields = context.get('product_fields', [])
        category_fields = context.get('category_fields', [])

        if product_fields != []:
            self.fields['product'] = CustomProductSerializer(read_only=True, fields=product_fields,
                                                             context=category_fields)
        return super().to_representation(instance)
