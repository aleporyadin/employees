def get_children_data(employees):
    children_data = []
    for employee in employees:
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
        children_data.append(data)
    return children_data