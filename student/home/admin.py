from django.contrib import admin
from .models import Student,Program,Student_Profile,CohortGroup

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name','last_name','status',  'get_cohort']

    def get_cohort(self, obj):
        cohort_group = obj.cohort.all() 
        return ", ".join([cohort.name for cohort in cohort_group])

    # Optional: Add a short description for the method (displayed as column title)
    get_cohort.short_description = 'Cohort'




@admin.register(Student_Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['student','date_of_birth', 'rating','address']

    


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['student', 'courses', 'grade']


   
@admin.register(CohortGroup)
class CohortAdmin(admin.ModelAdmin):
    list_display = ('name',)

    

# Register your models here.
# admin.site.register(Student)
# admin.site.register(Program)
# admin.site.register(Student_Profile)
# admin.site.register(CohortGroup)






