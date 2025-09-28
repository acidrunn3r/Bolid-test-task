import tempfile

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

# from rest_framework.renderers import JSONRenderer # Fix? for 405 error
from rest_framework.response import Response

from .filters import EventFilter
from .models import Event, Sensor
from .serializers import EventSerializer, SensorSerializer, UploadJSONSerializer
from .utils import import_events_from_json


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "id"]
    ordering = ["id"]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EventFilter
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="Импорт событий из JSON-файла",
        method="post",
        request_body=UploadJSONSerializer,
        responses={200: "Успешный импорт", 400: "Ошибка при импорте"},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="upload-json",
        # renderer_classes=[JSONRenderer] # Fix? for 405 error
    )
    def upload_json(self, request, *args, **kwargs):
        serializer = UploadJSONSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data["file"]
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_file:
                for chunk in uploaded_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name

            try:
                imported_ids = import_events_from_json(tmp_file_path)
                return Response(
                    {
                        "status": "ok",
                        "imported_count": len(imported_ids.get("imported", [])),
                        "imported_events": imported_ids,
                        "message": "Импорт завершён успешно.",
                    }
                )
            except Exception as e:
                return Response(
                    {"status": "error", "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
