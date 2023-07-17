$(document).ready(function () {
    $(document).on('click', '.employee-node', function () {
        const employeeId = $(this).data('employee-id');
        console.log(employeeId)
        const container = $(this).siblings('.children-container');

        if (container.children().length === 0) {
            $.get('/load-children/', {employee_id: employeeId}, (data) => {
                if (data.children) {
                    const ul = $('<ul>'); // Create the <ul> element

                    for (let i = 0; i < data.children.length; i++) {
                        const subordinate = data.children[i];
                        const li = $('<li>'); // Create the <li> element

                        // <img src="../static/assets/empl.svg" alt="Member">

                        const html = `
              <div class="employee-node member-view-box" data-employee-id="${subordinate.id}">
                <div class="member-image">
                  <div class="member-details">
                    <h5>${subordinate.full_name}</h5>
                    <p>${subordinate.position}</p>
                  </div>
                </div>
              </div>`;

                        li.html(html);
                        if (subordinate.has_children) {
                            const childContainer = $('<div class="children-container"></div>');
                            li.append(childContainer); // Append child container to the <li>
                        } else {
                            const end = $('<span>No subordinates</span>');
                            li.append(end);
                        }

                        ul.append(li);
                    }

                    container.append(ul);
                    container.show();
                }
            });
        } else {
            container.toggle(); // Toggle visibility of child elements
        }
    });
});
