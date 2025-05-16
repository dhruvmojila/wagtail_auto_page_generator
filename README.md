# Travel Website with Wagtail and Django

This is a modern travel website built using **Django** and **Wagtail** for managing and displaying routes, fares, airlines, and popular destinations. It leverages the flexibility of **Django** and the powerful content management system (CMS) capabilities of **Wagtail** to create a dynamic, user-friendly platform for displaying travel data.

## Features

- **Dynamic Route Pages**: Automatically generate pages for different source-destination routes using API data.
- **Airline Information**: Display which airlines serve specific routes.
- **Popular Routes**: Show popular flight search routes based on search frequency.
- **Customizable and Extendable**: Built with Django and Wagtail, easily extendable to add more features.

## Technologies Used

- **Django**: Python-based web framework for rapid development.
- **Wagtail**: Flexible CMS for managing content.
- **FastAPI**: For fetching travel data (routes, fares, airlines).
- **Tailwind CSS**: For a modern and responsive UI.
- **Python 3.x**: The programming language used for backend development.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Git
- Virtual Environment (recommended)

### Step 1: Clone the repository

Clone the project to your local machine using the following command:

```bash
git clone https://github.com/dhruvmojila/wagtail_auto_page_generator.git
````

### Step 2: Navigate to the project directory

```bash
cd wagtail_auto_page_generator
```

### Step 3: Set up a virtual environment

Create and activate a virtual environment to isolate your project dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 4: Install dependencies

Install all necessary dependencies with:

```bash
pip install -r requirements.txt
```

### Step 5: Set up the database

Run migrations to set up your database:

```bash
python manage.py migrate
```

### Step 6: Create a superuser (for admin access)

Create an admin user to access the Wagtail admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up the admin user.

### Step 7: Run the development server

Start the development server with:

```bash
python manage.py runserver
```

Your project should now be running at [http://localhost:8000](http://localhost:8000).

### Step 8: Access Wagtail Admin

To access the Wagtail admin panel, go to:

[http://localhost:8000/admin](http://localhost:8000/admin)

Log in using the superuser credentials you created earlier.

## Features

### 1. Dynamic Route Pages

Pages are dynamically created for different source and destination routes, fetching data from external APIs for route fares, airlines, and other information.

### 2. Airline Information

Each route page displays which airlines serve that specific route.

### 3. Popular Routes

A section that displays the most popular routes based on search frequency.

## Contributing

If you'd like to contribute to this project, feel free to open a pull request or file an issue with your suggestions. Please ensure that your contributions follow the project’s coding style and include tests where appropriate.

---

Happy coding! 😊
