from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializer import KarneSerializer, TermsSerializer, YearIndexSerializer, PdfFileSerializer
from .models import Karne, Terms, YearIndex, TermsList, InternList
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
                YearIndex.objects.create(year=grad_year)
            
            grad_status = calculate_grad_status(karne['student_id'], karne['terms'], karne['gno'])

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
                grad_year=grad_year,
                grad_status=grad_status
                )
            karne_model.save()

            Terms.objects.create(karne=karne_model, terms=karne['terms'])

def calculate_grad_status(student_id, terms, gno):
    # TODO: rewrite this mess after switching to the new format
    problem_array = []
    passes = True
    isInternPassed = True
    isHadSD = True
    isHadAD = True
    isTookLectures = True
    isPassedLetters = True
    letters_needed = ["AA", "BA", "BB", "CB", "CC", "DC", "DD", "BL"]
    if not InternList.objects.filter(student_id=student_id).exists():
        isInternPassed = False
    for i in range(8):
        lectures_needed = TermsList.objects.filter(term=str(i + 1) + 'YY').values_list('lecture_code')

        # ilk 4 yarıyıl için
        if i < 4:
            lectures_tmp = []
            for t in terms[i]:
                lectures_tmp.append(t['lecture_code'].replace("İ", "I"))
                #print(t['lecture_code'], normalize("NFKD", t['lecture_code']), normalize("NFD", t['lecture_code']), t['lecture_code'].replace("İ", "I"))
                # eğer ders kodu gerekli dersler içinde yok ise veya harf notu DD iken gno 2.5'dan küçük ise
                if not t['grade_letter'] in letters_needed or t['grade_letter'] == "DD" and gno < 2.5:
                    print("i", i, "have:", t['grade_letter'])
                    print("i", i, "have:", gno)
                    passes = False
                    isPassedLetters = False
                    problem_array.append({"lecture_code": t['lecture_code'], "lecture_name": t['lecture_name'], "grade_letter": t['grade_letter'], "gno": gno})

            # eger gerekli derslerden herhangi bir tanesi alınan derslerin içinde yok ise
            for l in lectures_needed:
                if not l[0] in lectures_tmp:
                    print("i", i, "have:", l[0], "needed:", lectures_tmp)
                    passes = False
                    isTookLectures = False
                    if isPassedLetters:
                        problem_array.append({"lecture_not_taken": l[0]})
        # son 4 yarıyıl için
        else:
            # seçimlik derslerin kodu
            lectures_needed_sd = TermsList.objects.filter(term=str(i + 1) + 'YYSD').values_list('lecture_code')
            lectures_needed_sd = [x[0] for x in lectures_needed_sd]

            # alan dışı seçimlik derslerin kodu
            lectures_needed_ad = TermsList.objects.filter(term=str(i + 1) + 'YYAD').values_list('lecture_code')
            lectures_needed_ad = [x[0] for x in lectures_needed_ad]

            # o dönemki alınan derslerin listesi
            lectures_tmp = []
            for t in terms[i]:
                lectures_tmp.append(t['lecture_code'].replace("İ", "I"))
                #print(t['lecture_code'], normalize("NFKD", t['lecture_code']), normalize("NFD", t['lecture_code']))
                # eğer ders kodu gerekli dersler içinde yok ise
                if not t['grade_letter'] in letters_needed or t['grade_letter'] == "DD" and gno < 2.5:
                    print("i", i, "have:", t['grade_letter'])
                    print("i", i, "have:", gno)
                    passes = False
                    isPassedLetters = False
                    problem_array.append({"lecture_code": t['lecture_code'], "lecture_name": t['lecture_name'], "grade_letter": t['grade_letter'], "gno": gno})
            for l in lectures_needed:
                if l[0] != 'XXX000' and not l[0] in lectures_tmp:
                    print("i", i, "have:", l[0], "needed:", lectures_tmp)
                    passes = False
                    isTookLectures = False
                    if isPassedLetters:
                        problem_array.append({"lecture_not_taken": l[0]})
            if i != 7:
                if len(list(set(lectures_tmp) & set(lectures_needed_sd))) != 2:
                    print("intersection test-sd:", "i", i, "have:", lectures_tmp, "needed:", set(lectures_needed_sd))
                    problem_array.append({"sd_not_taken_in_term": i+1})
                    passes = False
                    isHadSD = False
                if len(list(set(lectures_tmp) & set(lectures_needed_ad))) != 1:
                    problem_array.append({"ad_not_taken_in_term": i+1})
                    print("intersection test-ad:", "i", i, "have:", lectures_tmp, "needed:", set(lectures_needed_ad))
                    passes = False
                    isHadAD = False
            else:
                if len(list(set(lectures_tmp) & set(lectures_needed_sd))) != 3:
                    problem_array.append({"sd_not_taken_in_term": i+1})
                    print("intersection test-sd:", "i", i, "have:", lectures_tmp, "needed:", set(lectures_needed_sd))
                    passes = False
                    isHadSD = False
                if len(list(set(lectures_tmp) & set(lectures_needed_ad))) != 1:
                    problem_array.append({"ad_not_taken_in_term": i+1})
                    print("intersection test-ad:", "i:", i, "have:", set(lectures_tmp), "needed:", set(lectures_needed_ad))
                    passes = False
                    isHadAD = False
    problem_objects = {}
    for i in problem_array:
        problem_objects.update(i)
    status = {}
    status['isHadAD'] = isHadAD
    status['isHadSD'] = isHadSD
    status['isTookLectures'] = isTookLectures
    status['isPassedLetters'] = isPassedLetters
    status['passes'] = passes
    status['problems'] = problem_objects
    status['isInternPassed'] = isInternPassed

    return status

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
        query_result = Terms.objects.filter(karne_id=query_id)
        if not query_result.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = TermsSerializer(query_result, context={'request': request}, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
 
@api_view(['GET'])
def handleYearIndexQuery(request):
    query_result = YearIndex.objects.all()
    data = []
    if query_result.exists():
        serializer = YearIndexSerializer(query_result, context={'request': request}, many=True)
        data = serializer.data
    
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def handleRemoveRequests(request):
    try:
        request_ids = request.data['id']
        print(request_ids)
        request_year = request.data['year']
        print(request_year)
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        for id in request_ids:
            Karne.objects.filter(id=id).delete()

        # remove hanging years from the year index
        if not Karne.objects.filter(grad_year=request_year).exists():
            YearIndex.objects.filter(year=request_year).delete()

        return Response(status=status.HTTP_200_OK)
