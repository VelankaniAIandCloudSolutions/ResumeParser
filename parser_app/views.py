import datetime
import xlwt
from xlwt import Workbook, easyxf
from django.shortcuts import render, redirect
from pyresparser import ResumeParser
from .models import Resume, UploadResumeModelForm
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, FileResponse, Http404
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ResumeSerializer
def homepage(request):
    if request.method == 'POST':
        Resume.objects.all().delete()
        file_form = UploadResumeModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('resume')
        resumes_data = []
        if file_form.is_valid():
            for file in files:
                try:
                    # saving the file
                    resume = Resume(resume=file)
                    resume.save()
                    
                    # extracting resume entities
                    parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
                    data = parser.get_extracted_data()
                    resumes_data.append(data)
                    resume.name               = data.get('name')
                    resume.email              = data.get('email')
                    resume.mobile_number      = data.get('mobile_number')
                    if data.get('degree') is not None:
                        resume.education      = ', '.join(data.get('degree'))
                    else:
                        resume.education      = None
                    resume.company_names      = data.get('company_names')
                    resume.college_name       = data.get('college_name')
                    resume.designation        = data.get('designation')
                    resume.total_experience   = data.get('total_experience')
                    if data.get('skills') is not None:
                        resume.skills         = ', '.join(data.get('skills'))
                    else:
                        resume.skills         = None
                    if data.get('experience') is not None:
                        resume.experience     = ', '.join(data.get('experience'))
                    else:
                        resume.experience     = None
                    resume.save()
                except IntegrityError:
                    messages.warning(request, 'Duplicate resume found:', file.name)
                    return redirect('homepage')
            resumes = Resume.objects.all()
            messages.success(request, 'Resumes uploaded!')
            context = {
                'resumes': resumes,
            }
            return render(request, 'base.html', context)
    else:
        form = UploadResumeModelForm()
    return render(request, 'base.html', {'form': form})

def export_excel(request):
    response= HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Resumes' + \
        str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding = 'utf-8') 
    ws = wb.add_sheet('Resumes')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns= ['Resume File',
                'Name',
                'Email',
                'Mobile Number',
                'Education',
                'Total Experience in years',
                'Skills',
                'Experience']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Resume.objects.values_list('resume',
                'name',
                'email',
                'mobile_number',
                'education',
                'total_experience',
                'skills',
                'experience')
    for col in columns:
        print(col)
    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]),font_style)
    wb.save(response)

    return response


def resume_edit(request,id):
    resume = Resume.objects.get(pk=id)
    context = {
        'resume': resume,
        'values': resume
    }
    if request.method== 'GET':
        return render(request,'edit-resume.html',context)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        education = request.POST['education']
        total_experience = request.POST['total_experience']
        skills = request.POST['skills']
        experience = request.POST['experience']
    


        resume.name = name
        resume.email = email
        resume.mobile_number = mobile_number
        resume.education = education
        resume.total_experience = total_experience
        resume.skills = skills
        resume.experience = experience


        resume.save()
        messages.success(request, 'Updated  successfully')
        resumes = Resume.objects.all()
        return render(request, 'base.html',{
                'resumes': resumes,
            })

@api_view(['POST'])
def file_upload_view(request):
    Resume.objects.all().delete()
    files = request.FILES
    resumes_data = []
    response_data = []
    for index, file in enumerate(files):
        file_list  = request.FILES.getlist('resumes[' + str(index) + ']') 
        file = file_list[0]
        # with open('mediafiles/automhr_resumes/' + file.name, 'wb') as destination:
        #     for chunk in file.chunks():
        #         destination.write(chunk)
        resume = Resume(resume=file)
        resume.save()
        parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
        data = parser.get_extracted_data()
        resumes_data.append(data)
        resume.name               = data.get('name')
        resume.email              = data.get('email')
        resume.mobile_number      = data.get('mobile_number')
        if data.get('degree') is not None:
            resume.education      = ', '.join(data.get('degree'))
        else:
            resume.education      = None
        resume.company_names      = data.get('company_names')
        resume.college_name       = data.get('college_name')
        resume.designation        = data.get('designation')
        resume.total_experience   = data.get('total_experience')
        if data.get('skills') is not None:
            resume.skills         = ', '.join(data.get('skills'))
        else:
            resume.skills         = None
        if data.get('experience') is not None:
            resume.experience     = ', '.join(data.get('experience'))
        else:
            resume.experience     = None
        resume.save()
        response_data.append(resume)


    resume_serializer  = ResumeSerializer(response_data,many =True)
    return Response({'message': 'Files uploaded successfully',
                     'resumes': resume_serializer.data
                     })

@api_view(['POST'])
def test(request):
    print('run')
    return Response({"message": "Files uploaded successfully."})

# def file_upload2(request):
#     if request.method == 'POST':
#         print("hello")
#         Resume.objects.all().delete()
#         # file_form = UploadResumeModelForm(request.POST, request.FILES)
#         # files = request.FILES.getlist('resume')
#         my_files = request.FILES.getlist('file')
#         resumes_data = []
        
#         for file in my_files:
#             try:
#                     # saving the file
#                     resume = Resume(resume=file)
#                     resume.save()
                    
#                     # extracting resume entities
#                     parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
#                     data = parser.get_extracted_data()
#                     resumes_data.append(data)
#                     resume.name               = data.get('name')
#                     resume.email              = data.get('email')
#                     resume.mobile_number      = data.get('mobile_number')
#                     if data.get('degree') is not None:
#                         resume.education      = ', '.join(data.get('degree'))
#                     else:
#                         resume.education      = None
#                     resume.company_names      = data.get('company_names')
#                     resume.college_name       = data.get('college_name')
#                     resume.designation        = data.get('designation')
#                     resume.total_experience   = data.get('total_experience')
#                     if data.get('skills') is not None:
#                         resume.skills         = ', '.join(data.get('skills'))
#                     else:
#                         resume.skills         = None
#                     if data.get('experience') is not None:
#                         resume.experience     = ', '.join(data.get('experience'))
#                     else:
#                         resume.experience     = None
#                     resume.save()
#             except IntegrityError:
#                     messages.warning(request, 'Duplicate resume found:', file.name)
#                     return redirect('homepage')
#             resumes = Resume.objects.all()
#             messages.success(request, 'Resumes uploaded!')
#             context = {
#                 'resumes': resumes,
#             }
#             return render(request, 'base.html', context)
#     else:
    
#         return render(request, 'base.html')
