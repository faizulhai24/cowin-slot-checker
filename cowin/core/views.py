from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from cowin.common.cache.redis import redis
from cowin.common.helpers.otp_generator import generate_otp
from .models import User
from .serializers import UserSerializer
from .tasks import add_district_ids


class UserViewSet(GenericViewSet, RetrieveModelMixin):
    """ViewSet for User model"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        message_consent = request.data.get('message_consent')
        if not message_consent:
            return Response({'message': 'Message consent is required to register for notification.'},
                            status=HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        otp = generate_otp()
        redis.set(request.data['phone_number'], otp, 300)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(methods=['post'], url_path='otp/submit', detail=False)
    def otp_submit(self, request, **kwargs):
        otp = request.data.get('otp')
        phone_number = request.data.get('phone_number')

        if not otp or not phone_number:
            return Response({'message': 'OTP, Phone number is required.'}, status=HTTP_400_BAD_REQUEST)

        otp_in_cache = redis.get(phone_number)

        if not otp_in_cache:
            return Response({'message': 'OTP has expired, please try again.'}, status=HTTP_404_NOT_FOUND)

        if str(otp) != otp_in_cache.decode("utf-8"):
            return Response({'message': 'Incorrect OTP, please try again.'}, status=HTTP_401_UNAUTHORIZED)

        instance = self.queryset.filter(phone_number=phone_number).get()

        add_district_ids(instance.district_ids).delay()

        serializer = self.serializer_class(instance, data={'verified': True}, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
