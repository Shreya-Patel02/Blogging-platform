from django.shortcuts import redirect, render
from django.contrib import messages
from users.forms import RegistrationForm
from users.models import User
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def register_page(request):
    if not User.objects.exists():
        # Allow anyone to register when there are no users
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.role = 'Owner'  # First user gets the "Owner" role
                user.save()
                messages.success(request, "Registration successful! You are the Owner.")
                return redirect('login')
            else:
                messages.error(request, "Registration failed. Please correct the errors.")
        else:
            form = RegistrationForm()

        return render(request, 'users/register.html', {'form': form})
    else:
        # If there are users already, restrict registration to the "Owner" only
        @user_passes_test(lambda u: u.role == 'Owner', login_url='/login/')  # Only the Owner can access this
        def owner_register(request):
            if request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.role = form.cleaned_data['role']  # Assign the selected role from the form
                    user.save()
                    messages.success(request, "Registration successful!")
                    return redirect('login')
                else:
                    messages.error(request, "Registration failed. Please correct the errors.")
            else:
                form = RegistrationForm()

            return render(request, 'users/register.html', {'form': form})

        return owner_register(request)

def home_view(request):
    return render(request, 'base/base_generic.html')