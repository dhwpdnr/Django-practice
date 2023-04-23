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
