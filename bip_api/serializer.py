from rest_framework import serializers
from .models import Karne, Terms, YearIndex

class KarneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Karne
        fields = [
            'id',
            'university',
            'major',
            'student_id',
            'name',
            'surname',
            'signup_date',
            'print_date',
            'gno',
            'credits_sum',
            'points_sum',
            'grad_year',
        ]
class TermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = ['id', 'terms',]

class YearIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearIndex
        fields = ['id', 'year',]
 
class PdfFileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)
