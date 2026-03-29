simple-ecommerce-store/
├── manage.py
├── db.sqlite3
├── ecommerce/              # Main Django project
├── store/                  # Main app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── templates/
│   └── static/
└── venv/

step 1
## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/SomeshThombare/CodeAlpha_Simple_E-Commerce_store.git
   cd CodeAlpha_Simple_E-Commerce_store
step 2: create and active virtual environment
   python -m venv venv
venv\Scripts\activate     # Windows

step 3: Install dependence
pip install django

step 4: Apply migrations
python manage.py makemigrations
python manage.py migrate

step 5: Create superuser (Admin)Bash
python manage.py createsuperuser

step 6: Run the server
python manage.py runserver
