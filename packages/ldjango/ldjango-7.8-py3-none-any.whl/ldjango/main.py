import os
import secrets
import shutil
import subprocess
import sys
import time

import click
from tqdm import tqdm


def run_command(command, pbar):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pbar.update(1)
        time.sleep(0.5)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"\nError running command {' '.join(command)}:", fg="red"))
        click.echo(click.style(f"Exit code: {e.returncode}", fg="red"))
        click.echo(click.style(f"STDOUT: {e.stdout}", fg="yellow"))
        click.echo(click.style(f"STDERR: {e.stderr}", fg="red"))
        raise

def create_directory_structure(project_name):
    os.makedirs(project_name, exist_ok=True)
    os.makedirs(f"{project_name}/apps", exist_ok=True)
    os.makedirs(f"{project_name}/templates", exist_ok=True)
    os.makedirs(f"{project_name}/media", exist_ok=True)
    os.makedirs(f"{project_name}/static", exist_ok=True)

def create_django_project(project_name, pbar):
    try:
        result = subprocess.run(['django-admin', 'startproject', 'core', project_name], 
                                check=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)
        pbar.update(1)
        time.sleep(0.5)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"\nError creating Django project: {e.stderr}", fg="red"))
        click.echo(click.style("Make sure Django is installed and in your PATH.", fg="yellow"))
        click.echo(click.style("You can install Django using: pip install django", fg="yellow"))
        raise Exception("Failed to create Django project") from e

def create_django_apps(project_name, app_names, pbar):
    for app_name in app_names:
        app_path = f"{project_name}/apps/{app_name}"
        os.makedirs(app_path, exist_ok=True)
        try:
            run_command(['django-admin', 'startapp', app_name, app_path], pbar)
        except subprocess.CalledProcessError as e:
            click.echo(click.style(f"\nError creating app {app_name}: {e.stderr}", fg="red"))
            continue

        update_app_config(app_path, app_name)

def update_app_config(app_path, app_name):
    app_py = f"{app_path}/apps.py"
    if os.path.exists(app_py):
        with open(app_py, 'r') as file:
            content = file.read()
        content = content.replace(f"name = '{app_name}'", f"name = 'apps.{app_name}'")
        with open(app_py, 'w') as file:
            file.write(content)

def create_urls_file(project_name):
    urls_path = f"{project_name}/apps/urls.py"
    with open(urls_path, 'w') as file:
        file.write('from django.urls import path\nfrom ldjango.views import landing_page\n\nurlpatterns = [\n\tpath("", landing_page, name="landing_page")\n]\n')

def update_settings(project_name, app_names):
    settings_path = f"{project_name}/core/settings.py"
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as settings_file:
            settings_content = settings_file.read()
        
        settings_content = update_allowed_hosts(settings_content)
        settings_content = update_middleware(settings_content)
        settings_content = update_installed_apps(settings_content, app_names)
        settings_content = update_templates(settings_content)
        settings_content = add_static_and_media_settings(settings_content)

        with open(settings_path, 'w') as settings_file:
            settings_file.write(settings_content)
    else:
        raise FileNotFoundError(f"settings.py file not found in {settings_path}")

def update_allowed_hosts(content):
    allowed_hosts_pattern = "ALLOWED_HOSTS = []"
    if allowed_hosts_pattern in content:
        return content.replace(allowed_hosts_pattern, "ALLOWED_HOSTS = ['*']")
    return content

def update_middleware(content):
    middleware_pattern = 'MIDDLEWARE = ['
    whitenoise_middleware = "    'whitenoise.middleware.WhiteNoiseMiddleware',"
    if middleware_pattern in content and whitenoise_middleware not in content:
        insert_index = content.find(middleware_pattern) + len(middleware_pattern)
        return content[:insert_index] + f"\n{whitenoise_middleware}" + content[insert_index:]
    return content

def update_installed_apps(content, app_names):
    installed_apps_pattern = 'INSTALLED_APPS = ['
    if installed_apps_pattern in content:
        end_bracket_index = content.find(']', content.find(installed_apps_pattern))
        new_apps = '\n    ' + '\n    '.join([f"'apps.{app_name}'" for app_name in app_names])
        updated_content = content[:end_bracket_index].rstrip() + new_apps + '\n]' + content[end_bracket_index+1:]
        return updated_content.replace(",,", ",")
    return content

def update_templates(content):
    templates_pattern = "'DIRS': [],"
    if templates_pattern in content:
        return content.replace(templates_pattern, "'DIRS': [BASE_DIR / 'templates'],")
    return content

def add_static_and_media_settings(content):
    static_settings = """
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
"""
    if 'STATIC_URL' not in content:
        content += static_settings
    return content

def setup_tailwind(project_name, pbar):
    os.chdir(project_name)
    run_command(['npm', 'install', '-D', 'tailwindcss'], pbar)
    run_command(['npx', 'tailwindcss', 'init'], pbar)
    os.chdir('..')

    create_tailwind_config(project_name)
    create_tailwind_input_css(project_name)
    
    pbar.update(1)

def create_tailwind_config(project_name):
    tailwind_config = f"{project_name}/tailwind.config.js"
    tailwind_content = """/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html',
        './templates/*.html',
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}"""
    with open(tailwind_config, 'w') as config_file:
        config_file.write(tailwind_content)

def create_tailwind_input_css(project_name):
    os.makedirs(f"{project_name}/static/css", exist_ok=True)
    with open(f"{project_name}/static/css/input.css", 'w') as input_css:
        input_css.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;")

def build_tailwind_css(project_name, pbar):
    os.chdir(project_name)
    try:
        run_command(['npx', 'tailwindcss', '-i', './static/css/input.css', '-o', './static/css/output.css'], pbar)
    except KeyboardInterrupt:
        click.echo(click.style("Tailwind build process interrupted by user.", fg="yellow"))
    finally:
        os.chdir('..')
        
    pbar.update(1)

def create_base_html(project_name):
    base_html_content = """{% load static %}
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ldjango</title>
    <link href="{% static 'css/output.css' %}" rel="stylesheet">
    {% block head %}
    {% endblock %}
</head>

<body>
    {% block content %}
    {% endblock %}
    {% block footer %}
    {% endblock %}
</body>

</html>"""
    with open(f"{project_name}/templates/base.html", 'w') as base_html:
        base_html.write(base_html_content)

def copy_landing_page(project_name):
    ldjango_template_path = os.path.join(os.path.dirname(__file__), 'templates', 'landing_page.html')
    project_template_path = f"{project_name}/templates/landing_page.html"
    shutil.copy(ldjango_template_path, project_template_path)

def create_project_urls(project_name):
    urls_path = f"{project_name}/core/urls.py"
    with open(urls_path, 'w') as urls_file:
        urls_file.write('''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
''')

def run_django_commands(project_name, pbar):
    os.chdir(project_name)
    try:
        # Jalankan makemigrations terlebih dahulu
        subprocess.run(['python', 'manage.py', 'makemigrations'], check=True, capture_output=True, text=True)
        pbar.update(1)
        
        # Kemudian jalankan migrate
        migrate_result = run_command(['python', 'manage.py', 'migrate'], pbar)
        if migrate_result.returncode != 0:
            click.echo(click.style(f"Warning: Migration failed. Error:", fg="yellow"))
            click.echo(click.style(f"STDOUT: {migrate_result.stdout}", fg="yellow"))
            click.echo(click.style(f"STDERR: {migrate_result.stderr}", fg="red"))
            click.echo(click.style("You may need to run migrations manually after fixing any issues.", fg="yellow"))
        else:
            pbar.update(1)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error during Django commands: {e}", fg="red"))
        click.echo(click.style(f"STDOUT: {e.stdout}", fg="yellow"))
        click.echo(click.style(f"STDERR: {e.stderr}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred during Django commands: {str(e)}", fg="red"))
    
    try:
        subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput'], check=True, capture_output=True, text=True)
        pbar.update(1)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Warning: Collectstatic failed. Error:", fg="yellow"))
        click.echo(click.style(f"STDOUT: {e.stdout}", fg="yellow"))
        click.echo(click.style(f"STDERR: {e.stderr}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred during collectstatic: {str(e)}", fg="red"))
    
    try:
        with open('requirements.txt', 'w') as f:
            subprocess.run(['pip', 'freeze'], stdout=f, check=True)
        pbar.update(1)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Warning: Failed to generate requirements.txt. Error: {str(e)}", fg="yellow"))
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred while generating requirements.txt: {str(e)}", fg="red"))
    
    os.chdir('..')

def create_gitignore(project_name):
    with open(f"{project_name}/.gitignore", 'w') as gitignore:
        gitignore.write('''*.pyc
*.pyo
*.pyd
*.log
*.db
*.sqlite3
*.sqlite
*.sqlite-shm
*.sqlite-wal
*.DS_Store
./dist
./media
./node_modules
./venv
/media
/static
/node_modules
.hintrc
.env
''')

def display_success_message(project_name, app_names, use_tailwind, install_drf):
    click.echo(click.style(f"\n🎉 Congratulations! Project {project_name} has been successfully created with apps: {', '.join(app_names)}! 🎉", fg="green", bold=True))
    click.echo(click.style("Let's get your project up and running with these exciting steps:", fg="cyan"))
    
    click.echo(click.style(f"\n1. Open your project directory:", fg="yellow", bold=True))
    click.echo(click.style(f"   cd {project_name}", fg="magenta", italic=True))
    
    if use_tailwind:
        click.echo(click.style("\n2. Unleash the power of Tailwind CSS:", fg="yellow", bold=True))
        click.echo(click.style(f"   npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch", fg="magenta", italic=True))
        click.echo(click.style("   (Remember to close this terminal when you're done with the Tailwind magic!)", fg="yellow"))
    
    click.echo(click.style("\n3. Gather your static assets:", fg="yellow", bold=True))
    click.echo(click.style(f"   python manage.py collectstatic", fg="magenta", italic=True))
    
    click.echo(click.style("\n4. Launch your development server:", fg="yellow", bold=True))
    click.echo(click.style(f"   python manage.py runserver", fg="magenta", italic=True))
    
    if install_drf:
        click.echo(click.style("\n5. Django REST Framework has been installed. Check your settings and start building your API!", fg="yellow", bold=True))
    
    click.echo(click.style("\nYou're all set! Happy coding!", fg="green", bold=True))
def create_project_structure(project_name, app_names, use_tailwind, secret_key, install_drf):
    try:
        total_steps = 16 if install_drf else 15
        with tqdm(total=total_steps, desc=click.style("Creating project", fg="green", bold=True), unit="step", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            create_directory_structure(project_name)
            pbar.update(1)

            try:
                create_django_project(project_name, pbar)
            except Exception as e:
                click.echo(click.style(f"\nFailed to create Django project. Error: {str(e)}", fg="red"))
                return

            create_django_apps(project_name, app_names, pbar)
            create_urls_file(project_name)
            update_settings(project_name, app_names)
            create_env_files(project_name, secret_key)
            pbar.update(1)
            update_settings_for_env(project_name)
            pbar.update(1)

            if install_drf:
                install_django_rest_framework()
                update_settings_for_drf(project_name)
                create_serializers_and_views(project_name, app_names)
                pbar.update(1)

            if use_tailwind:
                setup_tailwind(project_name, pbar)
                build_tailwind_css(project_name, pbar)
            else:
                pbar.update(2)

            create_base_html(project_name)
            copy_landing_page(project_name)
            create_project_urls(project_name)
            
            run_django_commands(project_name, pbar)
            
            create_gitignore(project_name)

            while pbar.n < total_steps:
                pbar.update(1)
                time.sleep(0.1)

        display_success_message(project_name, app_names, use_tailwind, install_drf)
    except Exception as e:
        click.echo(click.style("\n❌ An error occurred during project creation.", fg="red", bold=True))
        click.echo(click.style(f"Error details: {str(e)}", fg="red"))
        click.echo(click.style(f"Error type: {type(e).__name__}", fg="red"))
        click.echo(click.style(f"Error location: {e.__traceback__.tb_frame.f_code.co_filename}, line {e.__traceback__.tb_lineno}", fg="red"))

def create_env_files(project_name, secret_key):
    env_path = f"{project_name}/.env"
    env_example_path = f"{project_name}/.env.example"
    
    env_content = f'''DEBUG=True
SECRET_KEY={secret_key}
DATABASE_URL=sqlite:///db.sqlite3
'''
    
    with open(env_path, 'w') as env_file:
        env_file.write(env_content)
    
    with open(env_example_path, 'w') as env_example_file:
        env_example_file.write(env_content.replace(secret_key, 'your-secret-key-here'))

def update_settings_for_env(project_name):
    settings_path = f"{project_name}/core/settings.py"
    with open(settings_path, 'r') as settings_file:
        settings_content = settings_file.read()
    
    # Hapus import yang sudah ada
    settings_content = settings_content.replace("from pathlib import Path", "")
    
    # Tambahkan import yang diperlukan
    new_imports = """
import environ
import os
from pathlib import Path
"""
    settings_content = new_imports + settings_content

    # Perbarui BASE_DIR
    base_dir_pattern = "BASE_DIR ="
    if base_dir_pattern in settings_content:
        start_index = settings_content.find(base_dir_pattern)
        end_index = settings_content.find("\n", start_index)
        settings_content = settings_content[:start_index] + "BASE_DIR = Path(__file__).resolve().parent.parent" + settings_content[end_index:]
    
    # Tambahkan konfigurasi environ
    environ_config = """
env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
"""
    settings_content = settings_content.replace("BASE_DIR = Path(__file__).resolve().parent.parent", "BASE_DIR = Path(__file__).resolve().parent.parent" + environ_config)
    
    # Perbarui SECRET_KEY
    secret_key_pattern = "SECRET_KEY ="
    if secret_key_pattern in settings_content:
        start_index = settings_content.find(secret_key_pattern)
        end_index = settings_content.find("\n", start_index)
        settings_content = settings_content[:start_index] + "SECRET_KEY = env('SECRET_KEY')" + settings_content[end_index:]
    
    # Perbarui DEBUG
    debug_pattern = "DEBUG ="
    if debug_pattern in settings_content:
        start_index = settings_content.find(debug_pattern)
        end_index = settings_content.find("\n", start_index)
        settings_content = settings_content[:start_index] + "DEBUG = env('DEBUG')" + settings_content[end_index:]
    
    # Perbarui DATABASES
    database_pattern = "DATABASES ="
    if database_pattern in settings_content:
        start_index = settings_content.find(database_pattern)
        end_index = settings_content.find("}", start_index)
        if end_index != -1:
            end_index = settings_content.find("\n", end_index)
            settings_content = settings_content[:start_index] + "DATABASES = {\n    'default': env.db(),\n}" + settings_content[end_index:]
    
    with open(settings_path, 'w') as settings_file:
        settings_file.write(settings_content)

def generate_secret_key():
    return secrets.token_urlsafe(50)

def install_django_rest_framework():
    packages = [
        "djangorestframework",
        "markdown",  # Markdown support for the browsable API.
        "django-filter",
        "djangorestframework-api-key==2.*"
    ]
    for package in packages:
        try:
            subprocess.Popen([sys.executable, "-m", "pip", "install", package], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
        except Exception as e:
            click.echo(click.style(f"Warning: Failed to install {package}. Error: {str(e)}", fg="yellow"))

def update_settings_for_drf(project_name):
    settings_path = f"{project_name}/core/settings.py"
    try:
        with open(settings_path, 'a') as settings_file:
            settings_file.write('''\nINSTALLED_APPS += [\n    'rest_framework',\n    'rest_framework_api_key',\n]\n''')
            settings_file.write('''\nREST_FRAMEWORK = {\n    "DEFAULT_PERMISSION_CLASSES": [\n        "rest_framework_api_key.permissions.HasAPIKey",\n    ],\n}\n''')
    except IOError as e:
        print(f"An error occurred while writing to settings.py file: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def create_serializers_and_views(project_name, app_names):
    for app_name in app_names:
        serializers_path = f"{project_name}/apps/{app_name}/serializers.py"
        views_path = f"{project_name}/apps/{app_name}/views.py"

        try:
            os.makedirs(os.path.dirname(serializers_path), exist_ok=True)
            os.makedirs(os.path.dirname(views_path), exist_ok=True)

            with open(serializers_path, 'w') as serializers_file:
                serializers_file.write(f"from rest_framework import serializers\n")
                serializers_file.write(f"from apps.{app_name}.models import *\n\n")
                serializers_file.write(f"# create your serializers\n")

            with open(views_path, 'w') as views_file:
                views_file.write(f"from django.shortcuts import render\n")
                views_file.write(f"from apps.{app_name}.models import *\n")
                views_file.write(f"from apps.{app_name}.serializers import *\n")
                views_file.write(f"from rest_framework import generics\n")
                views_file.write(f"from rest_framework_api_key.permissions import HasAPIKey\n\n")
                views_file.write(f"# Create your views here\n")
        except IOError as e:
            print(f"An error occurred while creating files for app {app_name}: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred for app {app_name}: {str(e)}")
            
    