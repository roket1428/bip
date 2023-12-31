from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializer import KarneSerializer, TermsSerializer, YearIndexSerializer, PdfFileSerializer
from .models import Karne, Terms, YearIndex
from .pdfparse import KarneParser

class handlePdfUpload(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser] 

    def create(self, request):
        serializer = PdfFileSerializer(data=request.data)
        if 'file' in request.FILES and serializer.is_valid():
            handleUploadedFiles(request)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

def handleUploadedFiles(request):
    file_list = request.FILES.getlist('file')
    for file in file_list:
        file_content = b''
        if file.multiple_chunks():
            chunk_size = 8192
            for chunk in file.chunks(chunk_size):
                file_content += chunk
        else:
            file_content = file.read()

        grad_year = request.data.get('year')
        karne_parser = KarneParser(file_content)
        karne = karne_parser.parse()
        if not Karne.objects.filter(student_id=int(karne['student_id']), grad_year=grad_year).exists():
            if not YearIndex.objects.filter(year=grad_year).exists():
                year_index_model = YearIndex(year=grad_year)
                year_index_model.save()

            terms_model = Terms(terms=karne['terms'])
            terms_model.save()

            karne_model = Karne(
                university=karne['university'],
                major=karne['major'],
                student_id=karne['student_id'],
                name=karne['name'],
                surname=karne['surname'],
                signup_date=karne['signup_date'],
                print_date=karne['print_date'],
                gno=karne['gno'],
                credits_sum=karne['credits_sum'],
                points_sum=karne['points_sum'],
                grad_year=grad_year
                )
            karne_model.save()


@api_view(['GET'])
def handleStudentListQuery(request):
    try:
        query_year = request.GET['year']
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        query_result = Karne.objects.filter(grad_year=query_year)
        if not query_result.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = KarneSerializer(query_result, context={'request': request}, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def handleTermQuery(request):
    try:
        query_id = request.GET['id']
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        query_result = Terms.objects.filter(id=query_id)
        if not query_result.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = TermsSerializer(query_result, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
 
@api_view(['GET'])
def handleYearIndexQuery(request):
    query_result = YearIndex.objects.all()
    if not query_result.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = YearIndexSerializer(query_result, context={'request': request}, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)