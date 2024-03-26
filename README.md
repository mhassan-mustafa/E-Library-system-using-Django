# E-Library system with Django

## Overview
This project is a dynamic E-Library web application developed using Django, aimed at managing extensive book records in a database. With a user-friendly interface crafted using HTML, CSS, Bootstrap, and JavaScript, it offers a seamless experience for readers.

## Features
- **Dynamic Web App**: Developed a dynamic E-Library web application using Django, facilitating easy management of book records.
- **User Registration and Authentication**: Implemented a user registration system with authentication to allow users to create accounts securely and log in to access the library's features.
- **Email Verification with OTP**: Engineered a hassle-free registration system with email verification through OTP to enhance security and ensure valid user registrations.
- **Book Request Feature**: Implemented an innovative feature allowing users to request books, with the application automatically delivering the requested book's PDF to the member's registered email.
- **Security Measures**: Ensured security measures such as password hashing and protection against common web vulnerabilities (e.g., CSRF protection) to safeguard user data and application integrity.
- **Vast Digital Collection**: Envisioned a mission to make reading accessible and convenient, offering a vast digital collection of books to transform the way readers engage with literature.

## Usage
1. **Clone the repository**:
```bash
git clone https://github.com/mhassan-mustafa/E-Library-system-using-Django
cd E-Library-system-using-Django
```


2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the Django application**:
```bash
python manage.py runserver
```

4. **Integrating Email System**:

   Integrate the email system for OTP verification and sending book request notifications

   Open the `e_library/settings.py` file in your Django project.

   Modify the following settings according to your email provider's specifications:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Change this port number according to your email provider's requirements
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'example@gmail.com'  # Replace 'example@gmail.com' with your email address
EMAIL_HOST_PASSWORD = 'your_password'  # Replace 'your_password' with your 16 charater pin
```


5. **Access the web application** through your browser at `http://localhost:8000`.

## File Structure
- **manage.py**: Django management script.
- **e_library/**: Django app directory.
- **models.py**: Contains Django models for book records.
- **views.py**: Defines view functions for handling HTTP requests.
- **forms.py**: Includes forms for user registration, book requests, etc.
- **urls.py**: Defines URL patterns for routing requests to views.
- **templates/**: Contains HTML templates for rendering views.
- **static/**: Holds static assets like CSS, JavaScript, and images.
- **README.md**: Documentation file providing an overview, features, usage instructions.
- **requirements.txt**: List of dependencies required for the project.

