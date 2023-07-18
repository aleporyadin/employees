from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from hierarchy.models import Employee

from hierarchy.utils import get_children_data


def index(request):
    return render(request, "index.html")


@login_required
def load_children(request):
    employee_id = request.GET.get('employee_id')

    try:
        employee = Employee.objects.get(id=employee_id)
        children = employee.get_children()
        data = []

        for child in children:
            data.append({
                'id': child.id,
                'full_name': child.full_name,
                'position': child.position,
                'hire_date': child.hire_date.strftime('%Y-%m-%d'),
                'email': child.email,
                'has_children': child.has_children()
            })

        return JsonResponse({'children': data})
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found.'}, status=404)


@login_required
def employees_data(request):
    directors = Employee.objects.filter(manager=None)
    employees = []

    for director_employee in directors:
        subordinates = director_employee.get_sub_employees()
        employees.append((director_employee, subordinates))

    return JsonResponse({'employees': employees})


@login_required
def employees_vertical(request):
    directors = Employee.objects.filter(manager=None)
    employees = []

    for director in directors:
        subordinates = director.get_sub_employees()
        employees.append((director, subordinates))

    return render(request, 'hierarchy/vertical.html', {'employees': employees})


@login_required
def employees_horizontal(request):
    directors = Employee.objects.filter(manager=None)
    employees = []

    for director_employee in directors:
        subordinates = director_employee.get_sub_employees()
        employees.append((director_employee, subordinates))

    return render(request, 'hierarchy/horizontal.html', {'employees': employees})


@login_required
def change_manager(request):
    employee_id = request.POST.get('employee_id')
    manager_id = request.POST.get('manager_id')

    try:
        employee = Employee.objects.get(id=employee_id)
        manager = Employee.objects.get(id=manager_id)
        employee.manager = manager
        employee.save()

        return JsonResponse({'success': True})
    except Employee.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Employee not found.'}, status=404)


@login_required
@require_POST
@csrf_exempt
def change_manager(request):
    dragged_employee_id = request.POST.get("dragged_employee_id")
    target_employee_id = request.POST.get("target_employee_id")

    try:
        dragged_employee = Employee.objects.get(id=dragged_employee_id)
        target_employee = Employee.objects.get(id=target_employee_id)

        # Update the employee's manager
        dragged_employee.manager = target_employee
        dragged_employee.save()

        return JsonResponse({'success': True})
    except Employee.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Employee not found.'}, status=404)
