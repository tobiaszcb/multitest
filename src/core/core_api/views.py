from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import TestSuiteSerializer, SingleTestSerializer
from ..models.test_dao import TestDAO


class GetLatestTestSuite(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        data = TestDAO().getLatestTestSuite()
        results = TestSuiteSerializer(data)
        return Response(results.data)


class GetLatestTest(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, name):
        data = TestDAO().getLatestTest(name)
        results = SingleTestSerializer(data)
        return Response(results.data)
