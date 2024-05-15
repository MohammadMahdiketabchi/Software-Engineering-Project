from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stu_no = models.CharField(verbose_name="Student Number", max_length=10, blank=False, null=False)
    is_ta = models.BooleanField(default=False)
    phone_no = models.CharField(verbose_name="Phone Number", blank=False, null=False)

class ProfessorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_no = models.CharField(verbose_name="National Number", max_length=10, unique=True, blank=False)
    students = models.ManyToManyField('StudentProfile', through='StudentProfessor', related_name='professors', default=None)
    def __str__(self):
        return f"{self.user} - {self.national_no}"
#intermediary model for adding some elemnts like datetime for relations if necessary
class StudentProfessor(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, default=None)
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.CASCADE, default=None)


#course model
def validate_zero_or_one(value):
    if value not in (0, 1):
        raise ValidationError("Value must be either 0 or 1.")

class ZeroOrOneField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [validate_zero_or_one]
        super(ZeroOrOneField, self).__init__(*args, **kwargs)
class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Course Name")
    term = models.IntegerField(verbose_name="Term")
    required_TAs = models.IntegerField(verbose_name="Required TAs")
    minPoint = models.IntegerField(verbose_name='minimum points')
    passCourse = ZeroOrOneField(verbose_name="should pass")
    description = models.TextField(verbose_name='description')
    professor = models.ForeignKey('ProfessorProfile', on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.name} - Term {self.term} - Section {self.professor}"
