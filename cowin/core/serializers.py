from rest_framework import serializers
from cowin.core.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'phone_number',
                  'first_name',
                  'state_id',
                  'district_ids',
                  'verified',
                  'message_consent',
                  'is_deleted'
                )
