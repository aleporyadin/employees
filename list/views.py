from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from hierarchy.models import Employee


# Create your views here.

@login_required
def employee_list(request):
    employees = Employee.objects.all()

    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by:
        if sort_by.startswith('-'):
            # Використовуємо "-" перед полем, якщо сортуємо у зворотному напрямку
            sort_by = sort_by[1:]
            employees = employees.order_by('-' + sort_by)
        else:
            employees = employees.order_by(sort_by)

    # Pagination
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'list.html', context)


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
    context = {'page_obj': page_obj, 'query': query}
    return render(request, 'list.html', context)
