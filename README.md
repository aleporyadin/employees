# TestApp

Tesp app for "АНЦ"

This project is a web application developed using Python, Django, JavaScript, jQuery, and Bootstrap.

## Setup

1. Clone the repository.
2. Install Python on your system.
3. Create a virtual environment: `python -m venv env`.
4. Activate the virtual environment:
    - For Windows: `.\env\Scripts\activate`
    - For macOS/Linux: `source env/bin/activate`
5. Install the required dependencies: `pip install -r requirements.txt`.
6. Create migrations: `python manage.py makemigrations`.
6. Run database migrations: `python manage.py migrate`.
7. Fill date base: `python manage.py fill 500`.
8. Start the development server: `python manage.py runserver`.

## Technologies Used

- Python
- Django
- JavaScript
- jQuery
- Bootstrap

## Project Structure

- `base.html`: The base HTML template that other templates extend from.
- `list.html`: A template for displaying the list of employees.
- `employee_rows.html`: A partial template for rendering employee rows in the list.
- `pagination.html`: A partial template for rendering pagination links.
- `employeeList.js`: JavaScript code for handling employee list functionality.
- `views.py`: Django views for handling employee-related requests.
- `models.py`: Django models for the Employee class.
- `urls.py`: URL configurations for the project.
- `settings.py`: Django project settings.

## Usage

1. Open the web application in your browser.
2. Sign in or sign up if you haven't already.
3. Navigate to the employee list page.
4. View, edit, or delete employees as necessary.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

@Oleksandr Poriadin