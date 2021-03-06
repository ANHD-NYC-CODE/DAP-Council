from rest_framework import serializers
from django.forms.models import model_to_dict

from core import models as c


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = c.Dataset
        fields = ('name', 'model_name', 'version', 'last_update', 'automated',
                  'update_schedule', 'records_start', 'records_end')

    last_update = serializers.SerializerMethodField()
    version = serializers.SerializerMethodField()

    def get_last_update(self, obj):
        update = obj.latest_update()

        if update:
            return update.completed_date

    def get_version(self, obj):
        return obj.latest_version()


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = c.UserMessage
        fields = ('from_email', 'description')
