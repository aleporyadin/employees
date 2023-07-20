async function fetchEmployees(employeeId) {
  return (await fetch(`/employees-list-without-selected/?employee_id=${employeeId}`, {method: 'POST'})).json();
}

$(document).ready(function () {

  const sortTableByColumn = (table, column, asc = true) => {
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll('tr'));

    const sortedRows = rows.sort((a, b) => {
      const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
      const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();

      return aColText.localeCompare(bColText) * dirModifier;
    });

    while (tBody.firstChild) {
      tBody.removeChild(tBody.firstChild);
    }

    tBody.append(...sortedRows);

    table.querySelectorAll('th').forEach(th => th.classList.remove('th-sort-asc', 'th-sort-desc'));
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle('th-sort-asc', asc);
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle('th-sort-desc', !asc);
  };

  document.querySelectorAll('.table th').forEach(headerCell => {
    headerCell.addEventListener('click', () => {
      const tableElement = headerCell.parentElement.parentElement.parentElement;
      const headerIndex = Array.from(headerCell.parentElement.children).indexOf(headerCell);
      const currentIsAscending = headerCell.classList.contains('th-sort-asc');

      sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    });
  });


  $('#editModal').on('show.bs.modal', event => {
    const button = event.relatedTarget;
    const employeeId = button.getAttribute('data-id');
    const modal = event.target;
    const managerListContainer = document.getElementById('edit-manager');

    fetch(`/get-employee/?employeeId=${employeeId}`)
      .then(response => response.json())
      .then(async data => {
        const {employee} = data;
        modal.querySelector('#edit-full-name').value = employee.full_name;
        modal.querySelector('#edit-position').value = employee.position;
        modal.querySelector('#edit-hire-date').value = employee.hire_date;
        modal.querySelector('#edit-email').value = employee.email;
        if (employee.manager_id) {
          const managers = (await fetchEmployees(employeeId)).employees;

          managers.forEach(manager => {
            const option = document.createElement('option');
            option.value = manager.id;
            option.text = manager.full_name;
            if (employee.manager_id && manager.id === employee.manager_id) {
              option.selected = true;
            }
            managerListContainer.appendChild(option);
          });
        }


      })
      .catch(error => {
        console.log(error);
      });

    $('#save-changes-btn').click(() => {
      const fullName = modal.querySelector('#edit-full-name').value;
      const position = modal.querySelector('#edit-position').value;
      const hireDate = modal.querySelector('#edit-hire-date').value;
      const email = modal.querySelector('#edit-email').value;
      const managerId = modal.querySelector('#edit-manager').value;
      const formData = new FormData();
      formData.append('fullName', fullName);
      formData.append('position', position);
      formData.append('hireDate', hireDate);
      formData.append('email', email);
      if (managerId) {
        formData.append('managerId', managerId);
      }
      formData.append('employeeId', employeeId);

      fetch('update-employee/', {
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(() => {
          location.reload();
        })
        .catch(error => {
          console.log(error);
        });

      $(modal).modal('hide');
    });
  }).on('hidden.bs.modal', event => {
    $('#edit-manager')
      .empty()
      .append('<option value="">No Manager</option>');
  });


  $('#deleteModal').bind('show.bs.modal', event => {
    const button = event.relatedTarget;
    const employeeId = button.getAttribute('data-id');
    const deleteBtn = document.getElementById('delete-modal-btn');
    const formData = new FormData();
    formData.append('employeeId', employeeId);
    deleteBtn.addEventListener('click', () => {
      console.log('asd');

      fetch('delete-employee/', {  // Update the URL here
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(() => {
          location.reload();
        })
        .catch(error => {
          console.log(error);
        });
      $('#deleteModal').modal('hide');
    });
  });
});