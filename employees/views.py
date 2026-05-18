import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder

from .models import Department, EmployeeProfile
from .forms import UserInfoForm, EmployeeProfileForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('directory')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'directory'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'employees/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def _get_or_create_profile(user):
    profile, _ = EmployeeProfile.objects.get_or_create(user=user)
    return profile


@login_required
def profile_edit(request):
    profile = _get_or_create_profile(request.user)
    if request.method == 'POST':
        user_form = UserInfoForm(request.POST, instance=request.user)
        profile_form = EmployeeProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile_edit')
    else:
        user_form = UserInfoForm(instance=request.user)
        profile_form = EmployeeProfileForm(instance=profile)
    return render(request, 'employees/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(User, pk=pk)
    profile = _get_or_create_profile(employee)
    return render(request, 'employees/employee_detail.html', {
        'employee': employee,
        'profile': profile,
    })


@login_required
def directory(request):
    query = request.GET.get('q', '').strip()
    if query:
        profiles = EmployeeProfile.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(job_title__icontains=query) |
            Q(department__name__icontains=query)
        ).select_related('user', 'department').order_by('user__last_name', 'user__first_name')
        return render(request, 'employees/directory.html', {
            'search_results': profiles,
            'query': query,
        })

    root_departments = Department.objects.filter(parent__isnull=True).prefetch_related(
        'employees__user', 'children'
    )
    unassigned = EmployeeProfile.objects.filter(department__isnull=True).select_related('user')
    return render(request, 'employees/directory.html', {
        'root_departments': root_departments,
        'unassigned': unassigned,
        'query': '',
    })


def _serialize_employee(profile):
    initials = (
        (profile.user.first_name[:1] + profile.user.last_name[:1]).upper()
        or profile.user.username[:2].upper()
    )
    return {
        'pk': profile.user.pk,
        'name': profile.display_name(),
        'title': profile.job_title or '',
        'email': profile.user.email,
        'phone': profile.phone or profile.mobile or '',
        'is_manager': profile.is_manager,
        'avatar': profile.avatar.url if profile.avatar else None,
        'initials': initials,
    }


def _serialize_dept(dept):
    employees = list(
        dept.employees.select_related('user')
        .order_by('-is_manager', 'user__last_name', 'user__first_name')
    )
    return {
        'id': dept.pk,
        'name': dept.name,
        'description': dept.description,
        'employees': [_serialize_employee(p) for p in employees],
        'children': [_serialize_dept(c) for c in dept.children.all().order_by('order', 'name')],
    }


@login_required
def org_tree(request):
    roots = Department.objects.filter(parent__isnull=True).order_by('order', 'name')
    unassigned = EmployeeProfile.objects.filter(department__isnull=True).select_related('user')
    tree_data = {
        'departments': [_serialize_dept(d) for d in roots],
        'unassigned': [_serialize_employee(p) for p in unassigned],
    }
    return render(request, 'employees/org_tree.html', {
        'tree_json': json.dumps(tree_data, cls=DjangoJSONEncoder),
    })