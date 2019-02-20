from rest_framework import serializers

class TestSuiteSerializer(serializers.Serializer):
    created = serializers.CharField()
    testSuiteId = serializers.CharField(max_length=100)
    duration = serializers.FloatField()
    is_finished = serializers.BooleanField()
    tests = serializers.ListField()

class SingleTestSerializer(serializers.Serializer):
    test_id = serializers.CharField()
    created = serializers.CharField()
    name = serializers.CharField()
    targetEnv = serializers.CharField()
    duration = serializers.FloatField()
    err = serializers.CharField()
    out = serializers.CharField()