from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from hierarchy.models import Employee

from hierarchy.utils import get_children_data


def index(request):
    return render(request, "index.html")


@login_required
def load_children(request):
    employee_id = request.GET.get('employee_id')
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)

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

@login_required
def employees_vertical(request):
    director = Employee.objects.filter(manager=None)
    subordinates = get_children_data(director)
    employees = zip(director, subordinates)

    return render(request, 'hierarchy/vertical.html', {'employees': employees})


@login_required
def employees_horizontal(request):
    director = Employee.objects.filter(manager=None)
    subordinates = get_children_data(director)
    employees = zip(director, subordinates)

    return render(request, 'hierarchy/horizontal.html', {'employees': employees})
