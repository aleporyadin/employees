from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from home.models import Employee


@login_required
def employee_list(request):
    search_query = request.GET.get('q')

    employees = Employee.objects.all()

    if search_query:
        employees = employees.filter(
            Q(full_name__icontains=search_query) |
            Q(position__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    sort_by = request.GET.get('sort')
    if sort_by:
        if sort_by.startswith('-'):
            sort_by = sort_by[1:]
            employees = employees.order_by('-' + sort_by)
        else:
            employees = employees.order_by(sort_by)

    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'search_query': search_query}
    return render(request, 'list/list.html', context)


@login_required
@csrf_exempt
def employees_list_without_selected(request):
    employees = Employee.objects.values('id', 'full_name').exclude(id=request.GET.get('employee_id'))
    return JsonResponse({'employees': list(employees)})


@login_required
def search_employees(request):
    query = request.GET.get('query')
    employees = Employee.objects.filter(
        Q(full_name__icontains=query) |
        Q(position__icontains=query) |
        Q(email__icontains=query) |
        Q(hire_date__icontains=query)
    )
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'list/list.html', context)

@login_required
def get_employee(request):
    employee_id = request.GET.get('employeeId')
    employee = get_object_or_404(Employee, id=employee_id)

    # Prepare the employee data to be sent as JSON response
    employee_data = {
        'id': employee.id,
        'full_name': employee.full_name,
        'position': employee.position,
        'hire_date': employee.hire_date.strftime('%Y-%m-%d'),
        'email': employee.email,
        'manager_id': employee.manager.id if employee.manager else None
    }

    return JsonResponse({'employee': employee_data})


@login_required
@csrf_exempt
def update_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employeeId')
        full_name = request.POST.get('fullName')
        position = request.POST.get('position')
        hire_date = request.POST.get('hireDate')
        email = request.POST.get('email')
        manager_id = request.POST.get('managerId')  # Get the manager ID from the request

        employee = get_object_or_404(Employee, id=employee_id)
        employee.full_name = full_name
        employee.position = position
        employee.hire_date = hire_date
        employee.email = email
        if manager_id:
            employee.manager_id = manager_id  # Set the manager ID

        employee.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


@login_required
@csrf_exempt
def delete_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employeeId')
        employee = get_object_or_404(Employee, id=employee_id)
        child_employees = employee.get_children()

        for child_employee in child_employees:
            child_employee.manager = employee.manager
            child_employee.save()

        with transaction.atomic():
            employee.delete()
            return JsonResponse({'success': True})

    return JsonResponse({'success': False})


@login_required
def load_more_managers(request):
    offset = int(request.GET.get('offset', 0))
    managers = Employee.objects.values('id', 'full_name')[offset:offset + 50]
    return JsonResponse({'managers': list(managers)})
