from django.shortcuts import render, redirect
# for login in authe
from django.contrib.auth import authenticate, login, logout

# for showing messagees of user successfully login in
from django.contrib import messages

from .forms import SignUpForm, AddRecordForm
from .models import CustomerRecord

# Create your views here.
def home(request):
	return render(request, 'home.html', {})

def admi(request):
    records = CustomerRecord.objects.all()

    # Check to see if logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # check username and password is is in databased
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('admi')
        else:
            messages.success(request, "There Was An Error Login In, Please Try Again")
            return redirect('admi')  
    else:
        return render(request, 'admin_.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have being logged out")
    return redirect('admi')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password = password)
            login(request, user)
            messages.success(request, "You have successfully Register")
            return redirect('admi')
    else:
        form = SignUpForm()

        return render(request, 'signup.html', {'form': form})
    
    return render(request, 'signup.html', {'form': form})


def customer_record(request, pk):
     #Every user must be authenticated
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = CustomerRecord.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('admi')



def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = CustomerRecord.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('admi')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('admi')


def add_record(request):
	form = AddRecordForm(request.POST or None)
	
	if request.method == "POST":
		if form.is_valid():
			# Check if a customer with the same email already exists
			email = form.cleaned_data['email']
			existing_customer = CustomerRecord.objects.filter(email=email).first()

			if existing_customer:
				messages.error(request, "A customer with this email already exists.")
				return redirect('add_record')
			else:
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
			
	return render(request, 'add_record.html', {'form':form})
	


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = CustomerRecord.objects.get(id=pk)
		# To make sure same record is passed before posting
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('admi')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('admi')