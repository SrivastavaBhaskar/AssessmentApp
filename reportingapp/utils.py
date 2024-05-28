from django.db.models import Max, Count, Sum
from django.forms import model_to_dict

from openpyxl import Workbook

from assessmentapp.models import AssessmentQuestionnaire

def get_overall_rating():
    totalWeight = AssessmentQuestionnaire.objects.all().aggregate(Sum('Weight'))
    totalRating = AssessmentQuestionnaire.objects.all().aggregate(Sum('Rating'))
    return (totalRating['Rating__sum']/totalWeight['Weight__sum']) * 5

def get_domainwise_rating(domain):
    totalWeight = AssessmentQuestionnaire.objects.filter(Domain=domain).aggregate(Sum('Weight'))
    totalRating = AssessmentQuestionnaire.objects.filter(Domain=domain).aggregate(Sum('Rating'))
    return (totalRating['Rating__sum']/totalWeight['Weight__sum']) * 5

def get_subdomainwise_rating(subDomain):
    totalWeight = AssessmentQuestionnaire.objects.filter(SubDomain=subDomain).aggregate(Sum('Weight'))
    totalRating = AssessmentQuestionnaire.objects.filter(SubDomain=subDomain).aggregate(Sum('Rating'))
    return (totalRating['Rating__sum']/totalWeight['Weight__sum']) * 5

def get_assessment_data():
    data = {}

    highestQuestionLevel = AssessmentQuestionnaire.objects.aggregate(Max('Level'))
    data['highestQuestionLevel'] = highestQuestionLevel['Level__max']

    totalDomains = AssessmentQuestionnaire.objects.aggregate(Count('Domain', distinct=True))
    data['totalDomains'] = totalDomains['Domain__count']

    data['overallRating'] = get_overall_rating()

    qs = AssessmentQuestionnaire.objects.all()
    
    domains = {}

    for question in qs:
        # print(question.Response)
        if question.Domain not in domains.keys():
            domains[question.Domain] = {
                'subDomains': {}
            } 
        if question.SubDomain not in domains[question.Domain]['subDomains'].keys():
            domains[question.Domain]['subDomains'][question.SubDomain] = {
                'yesQuestions': [],
                'noQuestions': [],
                'partialQuestions': [],
            }
        if question.Response == 'yes':
            domains[question.Domain]['subDomains'][question.SubDomain]['yesQuestions'].append(model_to_dict(question))
        if question.Response == 'no':
            domains[question.Domain]['subDomains'][question.SubDomain]['noQuestions'].append(model_to_dict(question))
        if question.Response == 'partial':
            domains[question.Domain]['subDomains'][question.SubDomain]['partialQuestions'].append(model_to_dict(question))
        # print(domains[question.Domain]['subDomains'][question.SubDomain])

    data['domains'] = domains

    for domain in domains.keys():
        # totalQuestions = AssessmentQuestionnaire.objects.filter(Domain=domain).aggregate(Count('SubDomain', distinct=True))
        data['domains'][domain]['totalSubDomains'] = len(domains[domain]['subDomains'].keys())
        data['domains'][domain]['totalQuestions'] = 0
        data['domains'][domain]['rating'] = get_domainwise_rating(domain)

        for subDomain in domains[domain]['subDomains'].keys():
            domains[domain]['subDomains'][subDomain]['yesCount'] = len(domains[domain]['subDomains'][subDomain]['yesQuestions'])
            domains[domain]['subDomains'][subDomain]['noCount'] = len(domains[domain]['subDomains'][subDomain]['noQuestions'])
            domains[domain]['subDomains'][subDomain]['partialCount'] = len(domains[domain]['subDomains'][subDomain]['partialQuestions'])
            domains[domain]['subDomains'][subDomain]['totalQuestions'] = len(domains[domain]['subDomains'][subDomain]['yesQuestions']) + len(domains[domain]['subDomains'][subDomain]['noQuestions']) + len(domains[domain]['subDomains'][subDomain]['partialQuestions'])
            domains[domain]['subDomains'][subDomain]['rating'] = get_subdomainwise_rating(subDomain)
            data['domains'][domain]['totalQuestions'] += domains[domain]['subDomains'][subDomain]['totalQuestions']

    # print(data)
    return data

def prepare_excel_data(data):
    excelData = {}
    Sheet1Data = []

    questions = AssessmentQuestionnaire.objects.all()
    tableHeader = list(model_to_dict(questions[0]).keys())
    Sheet1Data.append(tableHeader[1:])

    for question in questions[1:]:
        questiondetails = list(model_to_dict(question).values())

        Sheet1Data.append(questiondetails[1:])

    excelData['Sheet1Data'] = Sheet1Data

    Sheet2Data = [['Overall Rating', data['overallRating']],[], ['Domain', 'Rating']]

    for domain in data['domains'].keys():
        Sheet2Data.append([domain, data['domains'][domain]['rating']])

    Sheet2Data.append([])
    Sheet2Data.append(['Domain', 'Sub Domain', 'Rating'])

    for domain in data['domains'].keys():
        for subdomain in data['domains'][domain]['subDomains'].keys():
            Sheet2Data.append([domain, subdomain, data['domains'][domain]['subDomains'][subdomain]['rating']])

    # print(Sheet2Data)

    wb = Workbook()
    ws_home = wb.active
    ws_home.title = 'Questionnaire'

    for row in Sheet1Data:
        ws_home.append(row)

    ws_domain = wb.create_sheet('Domainwise Ratings')
    for row in Sheet2Data:
        ws_domain.append(row)

    wb.save('QuestionnaireData.xlsx')