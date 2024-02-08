from rest_framework import serializers, fields

from accounts.models import UserProfile


# https://stackoverflow.com/a/68561431/14665310
class IntegerDefaultField(fields.IntegerField):
    def get_attribute(self, instance):
        attibute = super().get_attribute(instance)
        if attibute is None and self.default != fields.empty:
            attibute = self.default
        return attibute


class ScoreboardSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    avg_score = IntegerDefaultField(default=0)
    total_score = IntegerDefaultField(default=0, source='score')

    class Meta:
        model = UserProfile
        fields = ['user', 'avg_score', 'total_score']
