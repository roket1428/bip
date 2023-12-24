from rest_framework import serializers
from .models import Karne

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
            'terms'
            'grad_date'
        ]
        
class PdfFileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)