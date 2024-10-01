from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.cats.serializers import BreedsSerializers, CatsSerializers, CatRatingSerializer
from apps.cats.models import Breeds, Cats, CatRating


class BreedsListView(generics.ListAPIView):
    queryset = Breeds.objects.all()
    serializer_class = BreedsSerializers


class CatsViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  # mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Cats.objects.all()
    serializer_class = CatsSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    ''' фильтрация по породе (url?cat={breed__id}) '''

    def list(self, request, *args, **kwargs):
        cat = self.request.GET.get('cat')
        queryset = self.get_queryset()
        if cat:
            queryset = queryset.filter(breed=cat)

        serializer = self.get_serializer(queryset, many=True).data
        return Response(serializer)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_cat(self, request, pk=None):
        try:
            instance = self.get_object()
            if instance.user != request.user:
                return Response(
                    {"response": False,
                     "message": "Короче брат, у тебя нет доптупа для удаления этого поста, с любовью кити точка ком)"
                     },
                    status=403
                )
            instance.delete()
            return Response({"response": True}, status=204)
        except Cats.DoesNotExist:
            return Response({"response": False}, status=404)

    @action(detail=True, methods=['patch'], url_path='update')
    def update_cat(self, request, pk=None):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"response": False,
                 "message": "Короче брат, у тебя нет доптупа для удаления этого поста, с любовью кити точка ком)"
                 },
                status=403
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)


class CatRatingView(generics.GenericAPIView):
    queryset = CatRating.objects.all()

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CatRatingSerializer(data=request.data)
        if CatRating.objects.filter(user=request.user, cat_id=request.data.get('cat')):
            return Response({"error": "Ты уже оценил котенка"}, status=400)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=401)
        return Response(serializer.errors, status=400)
