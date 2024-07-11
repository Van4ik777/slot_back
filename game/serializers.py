from rest_framework import serializers

class SpinRequestSerializer(serializers.Serializer):
    initial_money = serializers.IntegerField()
    stavka = serializers.IntegerField()

class SpinResponseSerializer(serializers.Serializer):
    l1 = serializers.ListField()
    l2 = serializers.ListField()
    l3 = serializers.ListField()
    money = serializers.IntegerField()
    winning_lines = serializers.ListField()
    multiplier = serializers.FloatField()
    message = serializers.CharField(required=False)
