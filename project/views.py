from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .Form import SummaryForm, MyForm
from .models import Summary


def Home(request):
    return render(request, 'project/home.html', {'Title': 'سرویس خلاصه ساز آنلاین'})


def loginuser(request):
    if request.method == 'GET':
        form = MyForm()
        return render(request, 'project/loginuser.html', { 'Title': 'ورود به سایت', 'form': form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
        if user is None:
            form = MyForm()
            return render(request, 'project/loginuser.html', {"form": form, 'error':'"نام کاربری یا رمز عبور اشتباه است"'})
        else:
            form = MyForm(request.POST)
            if form.is_valid():
                login(request, user)
                return redirect('home')
            else:
                form = MyForm()
                return render(request, "project/loginuser.html", {"form": form, 'error': '"اطلاعات را صحیح وارد کنید"'})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'project/signupuser.html', {'Title':'ثبت نام'})
    else:

        if request.POST['password1'] == request.POST['password2']:
            if len(request.POST['password1']) >= 8 and not(request.POST['password1'].isdigit()) and not (request.POST['password1'].isalpha()):
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('home')
                except IntegrityError:
                    return render(request, 'project/signupuser.html',
                                  {'error': '"این نام کاربری قبلا گرفته شده است. لطفا دوباره امتحان کنید"'})
            else:
                return render(request, 'project/signupuser.html',
                              { 'error': '"رمز عبور باید حداقل دارای 8 کاراکتر عددی و حروف باشد"'})
        else:
            return render(request, 'project/signupuser.html', {'error': '"رمز عبور و تکرار آن یکسان نیست"'})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def summaryServices(request):
    if request.method == 'GET':
        return render(request, 'project/summaryServices.html', {'Title': 'سرویس خلاصه ساز', 'form': SummaryForm()})
    else:
        try:
            form = SummaryForm(request.POST)
            newSummary = form.save(commit=False)
            newSummary.user = request.user
            newSummary.inputData = request.POST['text']
            out = ""
            for i in request.POST['text']:
                if i != '\n' or i != '\r':
                    out += i
            output = out.split()
            if len(output) >= 10:
                text = ""
                for i in range(10):
                    text += output[i]
                    text += ' '
                newSummary.outputData = text
            else:
                newSummary.outputData = request.POST['text']
            newSummary.save()
            return render(request, 'project/summaryServices.html', {'Title': 'سرویس خلاصه ساز', 'summary': newSummary.outputData})
        except ValueError:
            return render(request, 'project/summaryServices.html', {'error': 'bad data'})


def aboutUs(request):
    return render(request, 'project/aboutUS.html', {'Title': 'درباره ما'})

@login_required
def edit(request):
    if request.method == 'GET':
        return render(request, 'project/edit.html', {'Title': 'ویرایش اطلاعات'})
    else:
        if request.POST['password1'] == request.POST['password2']:
            if len(request.POST['password1']) >= 8 and not (request.POST['password1'].isdigit()) and not (request.POST['password1'].isalpha()):
                try:
                    user = user = authenticate(request, username=request.POST['old_username'], password=request.POST['old_password'])
                    user.delete()
                    user = User.objects.create_user(request.POST['New_username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('home')
                except IntegrityError:
                    return render(request, 'project/edit.html', {'error': 'این نام کاربری قبلا گرفته شده است. لطفا دوباره امتحان کنید.', 'Title': 'ویرایش اطلاعات'})
            else:
                return render(request, 'project/edit.html', {'error': 'رمز عبور باید حداقل دارای 8 کاراکتر عددی و حروف باشد', 'Title': 'ویرایش اطلاعات'})
        else:
            return render(request, 'project/edit.html', {'error':'رمز عبور و تکرار آن یکسان نیست.', 'Title': 'ویرایش اطلاعات'})

@login_required
def allsummaries(request):
    if request.method == 'GET':
        summaries = Summary.objects.filter(user=request.user)
        return render(request, 'project/allsummaries.html', {'Title': 'تاریخچه خلاصه ها', 'summaries': summaries})

@login_required
def viewsummaries(request, summary_pk):
    summary = get_object_or_404(Summary, pk=summary_pk, user=request.user)
    return render(request, 'project/viewsummaries.html', {'summary': summary})

@login_required
def deletesummary(request, summary_pk):
    summary = get_object_or_404(Summary, pk=summary_pk, user=request.user)
    if request.method == 'POST':
        summary.delete()
        return redirect('allsummaries')


