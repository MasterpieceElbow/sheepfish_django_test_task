from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    point_id = serializers.IntegerField()
    data = serializers.JSONField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def is_valid(self, *, raise_exception=False):
        order_data = self.initial_data["data"]
        if not all((
            isinstance(order_data, dict),
            order_data != {},
            *[isinstance(key, str) for key in order_data.keys()],
            *[isinstance(value, int) for value in order_data.values()],
        )):
            return False

        return super().is_valid(raise_exception=raise_exception)
