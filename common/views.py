from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  #가입 완료
            # 가입시 자동 로그인
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password1)
            login(request, user)  # 로그인
            return redirect('blog:index')
    else:
        form = UserForm()
    context = {'form':form}
    return render(request, 'common/signup.html', context)
