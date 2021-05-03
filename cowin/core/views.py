import logging
import re

from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet
from django.http import Http404

from cowin.common.cache.redis import redis
from cowin.common.helpers.otp_generator import generate_otp
from .models import User
from .serializers import UserSerializer
from .tasks import add_district_ids_to_cache, add_user_to_district_cache

logger = logging.getLogger(__name__)


class UserViewSet(GenericViewSet, RetrieveModelMixin):
    """ViewSet for User model"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        self.kwargs.update({'phone_number': self.kwargs[lookup_url_kwarg]})
        self.lookup_field = 'phone_number'

        if not re.match(r'[6789]\d{9}$', self.kwargs[lookup_url_kwarg]):
            raise ValueError("Invalid Phone number")
        return super(UserViewSet, self).get_object()

    def create(self, request, *args, **kwargs):
        message_consent = request.data.get('message_consent')
        if not message_consent:
            return Response({'message': 'Message consent is required to register for notification.'},
                            status=HTTP_400_BAD_REQUEST)

        logger.info(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        otp = generate_otp()
        logger.info("Generated otp {}".format(otp))
        redis.set(request.data['phone_number'], otp, 300)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
        except ValueError:
            return Response({'message': 'Invalid Phone number'}, status=HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'message': 'Number does not exist'}, status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['post'], url_path='vaccinated', detail=False)
    def vaccinated(self, request, **kwargs):
        phone_number = request.data.get('phone_number')

        if  not phone_number:
            logger.error('Phone number is required')
            return Response({'message': 'Phone number is required.'}, status=HTTP_400_BAD_REQUEST)
        try:
            instance = self.queryset.filter(phone_number=phone_number).get()
            serializer = self.serializer_class(instance, data={'is_deleted': True}, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'Number does not exist'}, status=HTTP_404_NOT_FOUND)

    @action(methods=['post'], url_path='otp/submit', detail=False)
    def otp_submit(self, request, **kwargs):
        otp = request.data.get('otp')
        phone_number = request.data.get('phone_number')

        if not otp or not phone_number:
            logger.error('OTP, Phone number is required')
            return Response({'message': 'OTP, Phone number is required.'}, status=HTTP_400_BAD_REQUEST)

        otp_in_cache = redis.get(phone_number)

        if not otp_in_cache:
            logger.error('OTP has expired, please try again')
            return Response({'message': 'OTP has expired, please try again.'}, status=HTTP_404_NOT_FOUND)

        if str(otp) != otp_in_cache.decode("utf-8"):
            return Response({'message': 'Incorrect OTP, please try again.'}, status=HTTP_401_UNAUTHORIZED)

        instance = self.queryset.filter(phone_number=phone_number).get()

        add_district_ids_to_cache(instance.district_ids).delay()
        add_user_to_district_cache(instance.id, instance.district_ids).delay()

        serializer = self.serializer_class(instance, data={'verified': True}, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
