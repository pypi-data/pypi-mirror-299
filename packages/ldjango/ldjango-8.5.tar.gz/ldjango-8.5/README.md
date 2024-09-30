# 🐍 ldjango: Your Django Project Assistant! 🚀

[![PyPI Version](https://badge.fury.io/py/ldjango.svg)](https://badge.fury.io/py/ldjango)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Tired of manually setting up Django projects? Introducing `ldjango` - your magic wand to create perfectly structured Django projects in a snap! 🪄✨


## 🎥 See ldjango in Action!

![ldjango Demo](https://raw.githubusercontent.com/lrndwy/ldjango/main/Screen%20Recording%20Sept%2026%20(1).gif)

See how ldjango makes creating Django projects easy and fast!



## 🌟 What's Special?

- **Swift Setup**: Create a complete structured Django project with just one command!
- **Smart App Creation**: Automatically create multiple Django apps!
- **Perfect Project Structure**: Get an organized project layout that even Marie Kondo would approve!
- **CLI Power**: Use intuitive command line options to customize your project creation.
- **Tailwind CSS Integration**: Enjoy the power of Tailwind CSS right out of the box!
- **Static Files**: Static files are automatically compiled and ready for production.
- **Media Files**: Media files are stored in a special folder for easy management.
- **Git Friendly**: Comes with a `.gitignore` file. Because we care about the cleanliness of your repository.
- **Special Static Folder**: Keep your static files organized and separate from your project.
- **HTML Template**: Use a basic HTML template to maintain consistency throughout your project.
- **Django Settings**: Well-organized settings file to manage your project configuration.
- **URL Routing**: Centralized URL routing system to manage all your app URLs.
- **Database**: Uses SQLite by default, but you can easily switch to your preferred database.
- **JavaScript Support**: Includes a `node_modules` folder to manage JavaScript dependencies.
- **NPM Scripts**: Use NPM scripts to compile your CSS and run other development tasks.
- **Django Commands**: Use Django commands to manage your project and apps.
- **Version Control**: Includes a `.gitignore` file to exclude unnecessary files from your repository.
- **Environment Variables**: Uses a `.env` file to store environment variables for your project.
- **Django REST Framework**: Option to install and configure Django REST Framework.
- **API Key**: Integration with djangorestframework-api-key for API security.
- **Automatic Serializer**: Automatically create serializer files for each app.
- **Advanced Customization**: Option to further customize your project structure.


## 🛠️ Installation

To get started with `ldjango`, follow these steps:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - For Windows:
     ```bash
     venv\Scripts\activate
     ```
   - For macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install `ldjango`:
   ```bash
   pip install ldjango
   ```

Now `ldjango` is ready to use in your virtual environment!

## 🚀 Quickstart

Launch your Django rocket with this command:

```bash
ldjango makeproject
```

Follow the prompts, and watch the magic happen! ✨

## 📚 Command Reference

- `ldjango makeproject`: Start the interactive project creation wizard
- `ldjango -h` or `ldjango --help`: Show help information
- `ldjango --version`: Show the version of ldjango you are using
- `ldjango generate-secret-key`: Generate a new secret key for Django

## 📁 Special ldjango: Project Structure

Your new Django project will look like this:

```
project_root/
│
├── apps/                       # Main folder containing all the applications in the Django project
│   ├── app1/                   # First application (app1) in the project
│   │   ├── migrations/         # Folder to store database migration files
│   │   ├── admin.py            # Configuration for Django's admin panel
│   │   ├── apps.py             # Configuration for the app in Django
│   │   ├── models.py           # Defines the database models for this app
│   │   ├── serializers.py      # Serializer for Django REST Framework
│   │   ├── tests.py            # File to write unit tests
│   │   ├── views.py            # Logic for handling views in this app
│
│   ├── app2/                   # Second application (app2) in the project
│   │   ├── ...                 # Same structure as app1
│
│   ├── More another apps/     # More apps in the project
│
│   ├── urls.py                 # URL routing for all the apps inside the `apps` folder
│
├── core/                       # Core folder containing overall project configuration
│   ├── asgi.py                 # ASGI configuration for running asynchronous servers
│   ├── settings.py             # Main configuration file for the Django project
│   ├── urls.py                 # Global URL routing for the entire project
│   ├── wsgi.py                 # WSGI configuration for running web servers
│
├── media/                      # Folder for storing user-uploaded files (images, documents, etc.)
│
├── node_modules/               # Folder containing JavaScript dependencies from npm (e.g., for Tailwind CSS)
│
├── static/                     # Folder for static files like CSS, JavaScript, and images
│   └── css/
│       ├── input.css           # Input CSS file (e.g., Tailwind CSS)
│       ├── output.css          # Output CSS file after processing
│
├── staticfiles/                # Folder to store static files that are ready for production
│   ├── admin/                  # Static files for Django's admin panel
│   └── css/                    # Additional CSS files for the app
│
├── templates/                  # Folder for storing HTML templates
│   ├── base.html               # Base HTML template for the application
│   ├── landing_page.html       # Landing page template for the application
│
├── .gitignore                  # File to specify files/folders that Git should ignore
├── .env                        # Environment variables for the project
├── .env.example                # Example environment variables for the project
├── db.sqlite3                  # SQLite database used by the project
├── manage.py                   # Command-line script to manage the Django project
├── package-lock.json           # File locking the versions of npm dependencies
├── package.json                # Configuration file for npm dependencies
├── requirements.txt            # File to specify Python dependencies
└── tailwind.config.js          # Configuration file for Tailwind CSS

```

## 🎭 Features That Will Make You Say "Wow!"

1. **App-tastic Organization**: All your apps are neatly placed inside the `apps` folder. No more app confusion!
2. **URL Mastery**: `urls.py` already configured inside the `apps` folder to manage all your app URLs.
3. **Ready, Set, Django**: `core` folder with all the essential Django project, ready to rock.
4. **Static & Media**: Special folders for your static and media files. Marie Kondo would be proud!
5. **Git Friendly**: Comes with a `.gitignore` file. Because we care about the cleanliness of your repository.
6. **Tailwind CSS Integration**: Enjoy the power of Tailwind CSS right out of the box!
7. **HTML Template**: Use a basic HTML template to maintain consistency throughout your project.
8. **Django Settings**: Well-organized settings file to manage your project configuration.
9. **Database**: Uses SQLite by default, but you can easily switch to your preferred database.
10. **JavaScript Support**: Includes a `node_modules` folder to manage JavaScript dependencies.
11. **NPM Scripts**: Use NPM scripts to compile your CSS and run other development tasks.
12. **Django Commands**: Use Django commands to manage your project and apps.
13. **Environment Variables**: Uses a `.env` file to store environment variables for your project.


## 🤔 Why Choose ldjango?

- **Highest Time Savings**: Say goodbye to repetitive project setup tasks.
- **Consistency Champion**: Every project follows the same, clean, and logical structure.
- **Best Friend for Beginners**: Perfect for Django beginners to start with the right steps.
- **Customization King**: Flexible enough to adapt to your unique project needs.
- **Tailwind CSS**: Tailwind CSS integrated into the project, so you can start styling your project right away.
- **Static Files**: Static files are automatically compiled and ready for production.
- **Media Files**: Media files are stored in a special folder for easy management.
- **Git Friendly**: Comes with a `.gitignore` file. Because we care about the cleanliness of your repository.
- **Special Static Folder**: Keep your static files organized and separate from your project.
- **HTML Template**: Use a basic HTML template to maintain consistency throughout your project.
- **Django Settings**: Well-organized settings file to manage your project configuration.
- **URL Routing**: Centralized URL routing system to manage all your app URLs.
- **Database**: Uses SQLite by default, but you can easily switch to your preferred database.
- **JavaScript Support**: Includes a `node_modules` folder to manage JavaScript dependencies.
- **NPM Scripts**: Use NPM scripts to compile your CSS and run other development tasks.
- **Django Commands**: Use Django commands to manage your project and apps.
- **Environment Variables**: Uses a `.env` file to store environment variables for your project.
- **Django REST Framework Integration**: Option to easily set up Django REST Framework.
- **API Security**: Integration with djangorestframework-api-key for better API security.
- **Automatic Serializer**: Automatically create serializer files to make API development easier.
- **Advanced Customization**: More options to customize the project to your needs.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact Us!

My Instagram - [@lrnd.__](https://instagram.com/lrnd.__)

Project Link: [ldjango](https://github.com/lrndwy/ldjango)

---

Ready to djangofy your development process? Try ldjango and watch your productivity soar! 🚀🐍