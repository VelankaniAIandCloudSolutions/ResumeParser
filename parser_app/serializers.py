from rest_framework import serializers

# try:
#     from course.serializers import CategorySerailizer
# except ImportError:
#     import sys
#     CategorySerailizer = sys.modules[__package__ + '.CategorySerailizer']
# 
# from course.serializers import CourseListSerializer

from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = (
            'id', 'resume', 'name', 'email', 'mobile_number', 'education',
            'skills', 'company_name', 'college_name', 'designation',
            'experience', 'uploaded_on', 'total_experience', 'get_resume',
        )


