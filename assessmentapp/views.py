from django.forms import modelformset_factory
from django.shortcuts import redirect, render

from assessmentapp.forms import AssessmentQuestionForm, InitiateAssessmentForm
from assessmentapp.models import AssessmentQuestionnaire
from assessmentapp.utils import clear_assessment_details, clear_questionnaire, process_excel
from reportingapp.views import reporting_view

# Create your views here.
def home_view(request):
    context = {}
    if request.method == 'POST':
        form = InitiateAssessmentForm(request.POST, request.FILES)
        if form.is_valid():
            clear_questionnaire()
            clear_assessment_details()
            file = request.FILES['AssessmentFile']
            process_excel(file)
            form.save()
            return redirect(assessment_view)
    form = InitiateAssessmentForm()
    context['form'] = form
    return render(request=request, template_name='home.html', context=context)

def assessment_view(request):
    context = {}
    questions = AssessmentQuestionnaire.objects.all()
    question_form_set = modelformset_factory(AssessmentQuestionnaire, form=AssessmentQuestionForm, extra=0)
    if request.method == 'POST':
        formset = question_form_set(request.POST, queryset=questions)
        if formset.is_valid():
            formset.save()
        return redirect(reporting_view)
    formset = question_form_set(queryset=questions)
    context['formset'] = formset
    return render(request=request, template_name='assessment.html', context=context)