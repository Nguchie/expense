from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Expenditure
from .forms import ExpenditureForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

def superuser_required(view_func):

    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return redirect('login')  # Redirect to login page if not a superuser
    return wrapper

@superuser_required
def home(request):
    expenditures = Expenditure.objects.all()
    return render(request, 'expenditure_list.html', {'expenditures': expenditures})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('home')  # Redirect to a protected view
        else:
            return HttpResponse('Invalid login ', status=401)
    return render(request, 'login.html')

def create_expenditure(request):
    if request.method == 'POST':
        form = ExpenditureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenditure_list')
    else:
            form = ExpenditureForm()
    return render(request, 'expenditure_form.html', {'form': form})




def expenditure_list(request):


    query = request.GET.get('q', '')
    if query:
        expenditures = Expenditure.objects.filter(
            #ename__icontains=query
            Q(ename__icontains=query) |
            Q(eamount__icontains=query) |
            Q(edate__icontains=query) |
            Q(issued_to__icontains=query)
        )

        if not expenditures:
            messages.info(request, "No items found matching your search criteria.")
    else:
        expenditures = Expenditure.objects.all()

    return render(request, 'expenditure_list.html', {'expenditures': expenditures})


def update_expenditure(request, pk):
    expenditure = get_object_or_404(Expenditure, pk=pk)
    if request.method == 'POST':
        form = ExpenditureForm(request.POST, instance=expenditure)
        if form.is_valid() :
            form.save()
            return redirect('expenditure_list')
    else:
            form = ExpenditureForm(instance=expenditure)
    return render (request, 'expenditure_form.html', {'form':form})

def delete_expenditure(request, pk):
    expenditure = get_object_or_404(Expenditure, pk=pk)
    if request.method == 'POST':
        expenditure.delete()
        messages.success(request, f"{expenditure.ename} was deleted successfully.")
        return redirect ('expenditure_list')
    return render(request, 'deleted_successfully.html', {'expenditure':expenditure} )


def export_expenditures_pdf(request):

    expenditures = Expenditure.objects.all()

    # Render HTML template with data
    html = render_to_string('expenditures_pdf.html', {'expenditures': expenditures})

    # Create a response object and set the content type to PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expenditures.pdf"'

    # Create a PDF from the HTML
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check if there was an error creating the PDF
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def custom_password_reset(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.html"
                    c = {
                        "email": user.email,
                        "domain": get_current_site(request).domain,
                        "site_name": "Your Site",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email_content = render_to_string(email_template_name, c)
                    send_mail(subject, email_content, 'admin@gmail.com', [user.email], fail_silently=False)


                # Instead of redirecting, display a message
                return render(request, "password_reset_form.html", {
                    "form": None,  # Remove the form
                    "success_message": "Password reset email has been sent to your email address.",
                })
            else:
                messages.error(request, "Email not found. Please try again.")
    else:
        form = CustomPasswordResetForm()

    return render(request, "password_reset_form.html", {"form": form})


def custom_password_reset_confirm(request, uidb64=None, token=None):
    if uidb64 is not None and token is not None:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if request.method == "POST":
                form = CustomSetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, user)  # Log the user in after password change
                    messages.success(request, "Password changed successfully")
                    return redirect('login')

            else:
                form = CustomSetPasswordForm(user)
        else:
            form = None
            messages.error(request, "The password reset link is invalid, possibly because it has already been used.")
    else:
        form = None
        messages.error(request, "Invalid reset link.")
    return render(request, "password_reset_confirm.html", {"form": form})