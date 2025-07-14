# kiran-s_clothing_shop

This is a full-stack Django-based eCommerce platform built to showcase a shirt store. It includes user registration, authentication, shirt listings, cart management, favorites, order placement, and a basic admin interface. The application demonstrates key aspects of web development, including models, views, templates, static/media handling, and database operations.

## Features

### User Functionality
- User registration and login
- Browse shirt listings with front and back images
- Add shirts to cart and manage quantities
- Add or remove shirts from favorites
- Place orders and view billing confirmation
- View login-required pages tailored to the authenticated user

### Admin Functionality
- Manage shirt inventory, sizes, stock, and images
- Manage user orders and cart contents
- Admin panel using Django’s built-in admin interface

### Media and UI
- Separate static and media file handling
- Banner slides for homepage
- Custom assets for login, register, and billing pages

## Tech Stack

- **Backend:** Python, Django  
- **Frontend:** HTML, CSS, Bootstrap  
- **Database:** SQLite  
- **Admin Interface:** Django Admin  

## Project Structure

```
.
├── mysite/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── myapp/                  # Main application logic
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/myapp/    # HTML templates
│   ├── static/myapp/       # Static and media files
│   └── migrations/
├── db.sqlite3              # Database file
├── manage.py               # Django management script
└── README.md               # Project documentation
```

## How to Run the Project

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/KIRANBABU-PEDDA/CLOTH-STORE
cd CLOTH-STORE

# Create and activate a virtual environment
python -m venv env
source env/bin/activate   # Windows: env\Scripts
ctivate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Author

**Kiran Babu P**  
Software Developer | Hyderabad, India  
1+ year experience in full stack development  
Skills: Python, Django, JavaScript, HTML, CSS, Git, CI/CD, PostgreSQL, MySQL

## Future Improvements

- Add filtering and sorting for shirt listings
- Implement search functionality
- Integrate a payment gateway
- Add pagination to product pages

## License

This project is created for educational and portfolio purposes. Free to use and modify for non-commercial projects.

