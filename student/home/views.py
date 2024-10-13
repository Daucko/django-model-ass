from os import name
from django.shortcuts import render, get_object_or_404

from .models import Student, Student_Profile, Program, CohortGroup

# Create your views here.

def index(request):
    student_list = Student.objects.all()
    context = {
        "students": student_list
    }
    return render(request, "home/index.html", context)


def about(request, id):
    student = get_object_or_404(Student, id=id)
    cohort_group = student.cohortgroup_set.first() # type: ignore
    if cohort_group:
        # cohort_members = Student.objects.filter(cohortgroup__name=cohort_group.name)
        cohort_members = Student.objects.filter(cohortgroup=cohort_group)
    else:
        cohort_members = Student.objects.none() 

    context = {
        "student": student,
        "cohort_members": cohort_members,
    }

    return render(request, "home/about.html", context)
