# JobTrack

JobTrack is a Django-based application designed to track and manage job applications efficiently.

## Features

- Track job applications and their status.
- Manage contacts and company information.
- Simple and intuitive interface for job seekers.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bilelzayane/jobtrack
   cd jobtrack
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

Access the application at `http://127.0.0.1:8000/`.

## Credits

Developed by [Bilel Zayane](https://github.com/bilelzayane) and [Oussema Gazzeh](https://github.com/ussemagazzah).
