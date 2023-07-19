$(document).ready(function () {
  // Click event for expanding/collapsing employees
  $(document).on('click', '.employee-node', function () {
    const container = $(this).siblings('.children-container');
    if (container.children().length === 0) {
      const employeeId = $(this).data('employee-id');
      loadSubordinates(container, employeeId);
    } else {
      container.toggle(); // Toggle visibility of child elements
    }
  });

  // Drag and drop events
  $(document).on('dragstart', '.employee-node', function (event) {
    event.originalEvent.dataTransfer.setData('text', $(this).data('employee-id'));
  });

  $(document).on('dragover', '.employee-node', function (event) {
    event.preventDefault();
    $(this).addClass('drag-over');
  });

  $(document).on('dragleave', '.employee-node', function () {
    $(this).removeClass('drag-over');
  });

  $(document).on('drop', '.employee-node', function (event) {
    event.preventDefault();
    $(this).removeClass('drag-over');

    const draggedEmployeeId = event.originalEvent.dataTransfer.getData('text');
    const targetEmployeeId = $(this).data('employee-id').toString();

    if (draggedEmployeeId === targetEmployeeId) return;

    const draggedElement = $(`[data-employee-id="${draggedEmployeeId}"]`);
    const targetContainer = $(this).siblings('.children-container');

    // Perform an AJAX request to update the employee's manager
    $.post('/change-manager/', {
      dragged_employee_id: draggedEmployeeId,
      target_employee_id: targetEmployeeId
    })
      .done(function (data) {
        // Update the tree structure on success
        if (targetContainer.length === 0) {
          const ul = $('<ul class="children-container"></ul>');
          ul.append($('<li>').append(draggedElement));
          $(event.target).after(ul);
        } else {
          if (!targetContainer.is(':visible')) {
            const li = $('<li>').append(draggedElement);
            const ul = $('<ul class="children-container"></ul>').append(li);
            targetContainer.replaceWith(ul);
          } else {
            targetContainer.append($('<li>').append(draggedElement));
          }
        }
      })
      .fail(function (xhr, status, error) {
        // Handle errors here if needed
        console.error(error);
      });
  });

  // Function to load subordinates via AJAX
  function loadSubordinates(container, employeeId) {
    $.get('/load-children/', { employee_id: employeeId })
      .done(function (data) {
        if (data.children) {
          for (let i = 0; i < data.children.length; i++) {
            const subordinate = data.children[i];
            const li = $('<li>'); // Create the <li> element
            const html = `
              <span class="employee-node" draggable="true" data-employee-id="${subordinate.id}">
                ${subordinate.full_name} (${subordinate.position}) ${!subordinate.has_children ? 'No subordinates' : ''}
              </span>`;
            li.html(html);
            if (subordinate.has_children) {
              const childContainer = $('<ul class="children-container droppable"></ul>');
              li.append(childContainer);
            }
            container.append(li);
          }
          container.show();
        }
      })
      .fail(function (xhr, status, error) {
        // Handle errors here if needed
        console.error(error);
      });
  }
});
