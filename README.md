# 📱 CodeAlpha Social Media Platform

A modern **Social Media Platform** built with **Django** as part of the CodeAlpha Internship.

---

## ✨ Features

### User Features
- User Registration and Login
- Create, Edit and Delete Posts
- Like and Comment on posts
- User Profile pages
- Follow/Unfollow other users
- View timeline (posts from followed users)
- Responsive and clean UI

### Admin Features
- Manage users, posts, comments and likes through Django Admin
- Full control over the platform

---

## 🛠️ Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite
- **Authentication**: Django's built-in User Authentication
- **Static Files**: CSS & JavaScript

---

## 📂 Project Structure
socialmedia/
├── manage.py
├── socialmedia/            # Main Django project
├── posts/                  # App for posts and feeds
├── accounts/               # App for user profiles & authentication
├── templates/
├── static/
└── venv/
text---

## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/SomeshThombare/CodeAlpha_Social_media_Platform.git
   cd CodeAlpha_Social_media_Platform

Create and activate virtual environmentBashpython -m venv venv
venv\Scripts\activate        # On Windows
Install dependenciesBashpip install django
Apply database migrationsBashpython manage.py makemigrations
python manage.py migrate
Create superuser (Admin)Bashpython manage.py createsuperuser
Run the development serverBashpython manage.py runserver
Open your browser and go to:texthttp://127.0.0.1:8000/


📸 Key Features Preview

User-friendly registration & login
Create text/image posts
Like ❤️ and comment 💬 on posts
Follow other users
Personalized feed
Clean and responsive design


🔮 Future Enhancements (Planned)

Image upload for posts
Real-time notifications
Direct messaging (DM)
Explore / Trending page
Dark mode
Deployment on Render / Railway


👤 Admin Access

Go to /admin/
Login with superuser credentials


📄 License
This project is developed as part of CodeAlpha Internship Program.

Made with ❤️ using Django
