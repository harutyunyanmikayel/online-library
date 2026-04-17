# Django Project

This is a Django-based small library web application.

## Setup Instructions

### 1. Install dependencies
Create a virtual environment and install required packages:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

python -m pip install -r requirements.txt
```

### 2. Run migrations
```bash
python manage.py migrate
```
### 3. Start the development server
```bash
python manage.py runserver
```

-----------------------------------------------------------------------------------------

Admin Access (Testing) 
A default superuser has already been created for testing purposes: 
- Username: admin 
- Password: test

This was created for local/testing use only.

If you want to create your own admin account, run:
```bash
python manage.py createsuperuser
```

**Notes**
Make sure your virtual environment is activated before running commands.
If you encounter missing dependencies, install them using requirements.txt.