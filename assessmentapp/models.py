from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class AssessmentDetails(models.Model):
    OrgName = models.CharField(max_length=125, blank=True, null=True)
    ProjectName = models.CharField(max_length=125, blank=True, null=True)
    ApplicationName = models.CharField(max_length=125, blank=True, null=True)
    AssessmentFile = models.FileField(validators=[FileExtensionValidator(
        ['xlsx']
    )])

    def __str__(self):
        return f'''Organization: {self.OrgName}\n
Project: {self.ProjectName}\n
Application: {self.ApplicationName}\n
'''

class AssessmentQuestionnaire(models.Model):
    RESPONSE_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
        ("partial", "Partial"),
    ]
    Domain = models.CharField(max_length=150, blank=True, null=True)
    SubDomain = models.CharField(max_length=150, blank=True, null=True)
    Question = models.CharField(max_length=500)
    Description = models.CharField(max_length=500, blank=True, null=True)
    Level = models.IntegerField(default=1)
    Weight = models.FloatField()
    Remediation = models.CharField(max_length=500, blank=True, null=True)
    Risk = models.CharField(max_length=500, blank=True, null=True)
    Response = models.CharField(max_length=30, choices=RESPONSE_CHOICES, default="no", blank=True, null=True)
    Remarks = models.CharField(max_length=500, blank=True, null=True)
    Rating = models.FloatField(default=0)
    
    def __str__(self):
        return self.Question + ' - ' + self.Response
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.Weight = 0.25 * self.Level
        if self.Response == 'no':
            self.Rating = 0
        elif self.Response == 'yes':
            self.Rating = self.Weight
        else:
            self.Rating = 0.5 * self.Weight
        if update_fields is not None and "Response" in update_fields:
            update_fields = {"Rating"}.union(update_fields)
        if update_fields is not None and "Level" in update_fields:
            update_fields = {"Weight"}.union(update_fields)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )