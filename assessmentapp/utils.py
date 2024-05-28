import openpyxl

from assessmentapp.models import AssessmentDetails, AssessmentQuestionnaire

def process_excel(filedata):
    wb = openpyxl.load_workbook(filedata)
    worksheet = wb["Sheet1"]
    excel_data = []
    for row in worksheet.iter_rows():
        if "Domain" in row[0].value:
            print([str(cell.value) for cell in row])
            continue
        row_data = [str(cell.value) for cell in row]
        excel_data.append(row_data)
        question = AssessmentQuestionnaire()
        if row[0].value != None:
            question.Domain = row[0].value
        if row[1].value != None:
            question.SubDomain = row[1].value
        if row[2].value != None:
            question.Question = row[2].value
        if row[3].value != None:
            question.Description = row[3].value
        if row[4].value != None:
            question.Level = row[4].value
        if row[5].value != None:
            question.Remediation = row[5].value
        if row[6].value != None:
            question.Risk = row[6].value
        if row[7].value != None:
            question.Response = row[7].value.lower()
        if row[8].value != None:
            question.Remarks = row[8].value

        question.save()

def clear_questionnaire():
    AssessmentQuestionnaire.objects.all().delete()

def clear_assessment_details():
    AssessmentDetails.objects.all().delete()