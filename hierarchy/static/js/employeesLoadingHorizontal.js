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
                        const html = `
                        <span class="employee-node" data-employee-id="${subordinate.id}">
${subordinate.full_name} (${subordinate.position}) ${!subordinate.has_children ? "No subordinates" : ''}</span>`;

                        li.html(html);
                        if (subordinate.has_children) {
                            const childContainer = $('<div class="children-container"></div>');
                            li.append(childContainer);
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
