from django.shortcuts import render

from assessmentapp.models import AssessmentDetails, AssessmentQuestionnaire
from reportingapp.utils import get_assessment_data, prepare_excel_data

# Create your views here.
def reporting_view(request):
    context = {}
    basic_details = AssessmentDetails.objects.first()
    context['orgName'] = basic_details.OrgName
    context['projectName'] = basic_details.ProjectName
    context['applicationName'] = basic_details.ApplicationName
    context['data'] = get_assessment_data()
    context['questions'] = AssessmentQuestionnaire.objects.exclude(Response='yes').order_by('Response')
    prepare_excel_data(context['data'])
    return render(request=request, template_name='reporting.html', context=context)

def generate_report_view(request):
    context = {}
    return render(request=request, template_name='generate_report.html', context=context)