from rest_framework.serializers import ModelSerializer, BooleanField
from drf_writable_nested import WritableNestedModelSerializer

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ('order', )


class OrderSerializer(WritableNestedModelSerializer, ModelSerializer):
    items = OrderItemSerializer(many=True)
    is_paid = BooleanField(read_only=True)


    class Meta:
        model = Order
        fields = ("id", "is_paid", "created_at", "total_price", "items")

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)

    def validate_items(self, items):
        print(items)
        return items