from rest_framework import status
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializer import PdfFileSerializer

class handlePdfUpload(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser] 

    def create(self, request):
        serializer = PdfFileSerializer(data=request.data)
        if 'file' in request.FILES and serializer.is_valid():
            #handleUploadedFiles(request.FILES.getlist('file'))
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

def handleUploadedFiles(file_list):
    # TODO: parse uploaded data and save it to the database
    pass