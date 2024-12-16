from os import name
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.decorators import login_required


from .models import Student, Student_Profile, CohortGroup, student_types

# Create your views here.

@login_required(login_url="/login")
def index(request):
    students = Student.objects.all()
    cohorts = CohortGroup.objects.all()
    paginator = Paginator(students, 3) 

    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    context = {
        "page_obj": page_obj,
        "cohorts": cohorts,
        "student_rank": student_types
    }

    return render(request, "home/index.html", context)


def about(request, slug):
    try:
        student = Student.objects.get(slug=slug)
    except Student.DoesNotExist:
        return redirect('404')
    
    cohort_group = student.cohort.first() # type: ignore
    if cohort_group:
        cohort_members = Student.objects.filter(cohort=cohort_group)
    else:
        cohort_members = Student.objects.none() 

    context = {
        "student": student,
        "cohort_members": cohort_members,
    }

    

    return render(request, "home/about.html", context)
    

def error404(request):
    return render(request, "home/404.html")


def send_message(request, id):
    if request.method == "POST":
        # Extract form data
        recipient_name = request.POST.get("recipient_name")
        recipient_email = request.POST.get("recipient_email")
        email_title = request.POST.get("email_title")
        message_body = request.POST.get("message_body")
        sender_name = request.POST.get("sender_name")
        sender_contact = request.POST.get("sender_contact")
        sender_email = request.POST.get("sender_email")

        # Validate the recipient's email
        try:
            validate_email(recipient_email)
        except ValidationError:
            messages.error(request, "Invalid email format. Please check the recipient's email address.")
            return redirect(reverse("about", args=[id]))

        # Construct the message content for the recipient
        recipient_message = (
            f"Message from {sender_name} ({sender_contact}, {sender_email}):\n\n"
            f"{message_body}"
        )

        # Construct the confirmation message for the sender
        sender_confirmation_message = (
            f"Hello {sender_name},\n\n"
            f"Your message to {recipient_name} ({recipient_email}) was successfully sent.\n\n"
            f"---\nSubject: {email_title}\n\n{message_body}\n---\n\n"
            f"Thank you for using our service!"
        )

        # Attempt to send both emails
        try:
            # Send email to the recipient
            send_mail(
                subject=email_title,
                message=recipient_message,
                from_email=sender_email,
                recipient_list=[recipient_email],
                fail_silently=False,
            )
            
            # Send confirmation email to the sender
            send_mail(
                subject="Your message was sent successfully",
                message=sender_confirmation_message,
                from_email="noreply@yourdomain.com",  # Use a no-reply or system email address
                recipient_list=[sender_email],
                fail_silently=False,
            )

            # Notify the sender in the application
            messages.success(request, "Message sent successfully! A confirmation email has been sent to you as well.")

        except Exception as e:
            # Display an error message if any email fails to send
            messages.error(request, f"Failed to send the message. Error: {e}")

        # Redirect back to the "about" page for the specified student
        return redirect(reverse("about", args=[id]))

    # Handle GET requests by redirecting to the "about" page
    return redirect(reverse("about", args=[id]))


class DeleteView(View):
    def get(self, request, slug):
        students   =  get_object_or_404(Student, slug=slug)
        students.delete()
        return redirect('index')
    

class Add_Students(View):
    def post(self, request):
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname  = request.POST.get('lastname')
        role =     request.POST.get('role')
        cohort_id = request.POST.get('cohort')
        courses = request.POST.get('courses')
        bio =  request.POST.get('bio')
        dob = request.POST.get('dob')
        address =request.POST.get('address')
        rating = request.POST.get('rating')
        profile = request.FILES.get('profile_images')

        print(bio)
        print(dob)
        print(address)
        print(rating)
        print(profile)

        
        if not username:
            return HttpResponse('username field  is required')
        
        if not bio:
            return HttpResponse('about field  is required')
        
        if not rating:
            return HttpResponse('rating field  is required')
        
        if Student.objects.filter(username=username).exists():
            return HttpResponse('username already taken')
        
        if not role:
            return HttpResponse('role field  is required')
        
       


        #create student
        students =  Student.objects.create(
             username=username,
            first_name=firstname, 
            last_name =lastname,
            student_type  = role
        )

        Student_Profile.objects.create(
            student=students,
            bio = bio,
            date_of_birth=dob,
            address=address,
            rating = rating,
            profile_picture  = profile
        )
        return redirect('index')
