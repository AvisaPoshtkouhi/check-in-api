from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from snippets.models import Visit, User, Location
from snippets.serializers import VisitSerializer, UserSerializer
from rest_framework.views import APIView
from datetime import datetime


class VisitList(APIView):
    def get(self, request):
        visit = Visit.objects.all()
        serializer = VisitSerializer(visit, many=True)
        return JsonResponse(serializer.data, safe=False)


class VisitCheckIn(APIView):
    def post(self, request, pk):
        data = JSONParser().parse(request)
        data['location_id'] = pk
        data['date'] = datetime.now()
        data['user_id'] = request.user.id
        serializer = VisitSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitDetails(APIView):
    def get(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = VisitSerializer(visit)
        return JsonResponse(serializer.data)

    def patch(self, request, pk):
        return self.put(request, pk)

    def put(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        serializer = VisitSerializer(visit, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        visit.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class UserVisits(APIView):
    def get(self, request, pk):
        try:
            User.objects.get(pk=pk)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        visits = Visit.objects.all().filter(user_id=pk)
        count = visits.count()
        avg = 0.0
        locations = []
        for visit in visits:
            avg += visit.ratio
            locations.append({'id': visit.location_id.id})

        return JsonResponse({'count': count,
                             'avg': round(avg / count, 2),
                             'locations': locations}, status=status.HTTP_200_OK)


class LocationVisits(APIView):
    def get(self, request, pk):
        try:
            Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        visits = Visit.objects.all().filter(location_id=pk)
        count = visits.count()
        avg = 0.0
        users = []
        for visit in visits:
            avg += visit.ratio
            users.append({'id': visit.user_id.id})

        return JsonResponse({'count': count,
                             'avg': round(avg / count, 2),
                             'visitors': users}, status=status.HTTP_200_OK)
