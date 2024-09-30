import os
import shutil
import signal
import sys
import time

import click
from colorama import Fore, Style, init

from .main import create_project_structure

version = '8.3'

# Initialize colorama
init(autoreset=True)

# ASCII art for LDJANGO with colors
LDJANGO_ASCII = f"""
   __     _  _                         
  / /  __| |(_) __ _ _ __   __ _  ___  
 / /  / _` || |/ _` | '_ \ / _` |/ _ \ 
/ /__| (_| || | (_| | | | | (_| | (_) |
\____/\__,_|/ |\__,_|_| |_|\__, |\___/ 
          |__/             |___/       c
"""

def display_ascii_art():
    for i in range(len(LDJANGO_ASCII)):
        print(f"{Fore.GREEN}{Style.BRIGHT}{LDJANGO_ASCII[i]}{Style.RESET_ALL}", end='', flush=True)
        time.sleep(0.001)
    print()

project_name = ""

def signal_handler(sig, frame):
    print(f"\n{Fore.YELLOW}Oops! Project creation interrupted. Time to clean up our magical mess...{Style.RESET_ALL}")
    if os.path.exists(project_name):
        shutil.rmtree(project_name)
        print(f"{Fore.GREEN}Poof! The project folder '{project_name}' has vanished into thin air.{Style.RESET_ALL}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

@click.group()
@click.version_option(version=version, message=f'{LDJANGO_ASCII}\n{Fore.GREEN}ldjango version {version}{Style.RESET_ALL}')
@click.help_option('-h', '--help')
def cli():
    """ldjango: CLI tool for creating Django projects with a predefined structure."""
    display_ascii_art()
    pass

@cli.command()
def makeproject():
    """Create a new Django project with a predefined structure."""
    global project_name
    click.echo(f"{Fore.YELLOW}{Style.BRIGHT}Welcome to ldjango: Your Django project creator!{Style.RESET_ALL}")
    
    project_name = click.prompt(f"{Fore.CYAN}{Style.BRIGHT}? {Fore.MAGENTA}{Style.NORMAL}Enter your project name{Style.RESET_ALL}", default="MyProject", prompt_suffix=": ", show_default=True)
    
    app_count = click.prompt(
        f"{Fore.CYAN}{Style.BRIGHT}? {Fore.MAGENTA}{Style.NORMAL}How many applications do you want to create?{Style.RESET_ALL}",
        type=click.IntRange(min=1),
        default=1,
        show_default=True,
        prompt_suffix=': ',
    )
    
    app_names = []
    for i in range(app_count):
        app_name = click.prompt(
            f"{Fore.CYAN}{Style.BRIGHT}? {Fore.MAGENTA}{Style.NORMAL}Django Application Name {i + 1}{Style.RESET_ALL}",
            default=f"MyApp{i + 1}",
            prompt_suffix=": ",
            show_default=True,
        )
        app_names.append(app_name)

    use_tailwind = click.confirm(f"{Fore.CYAN}{Style.BRIGHT}? {Fore.MAGENTA}{Style.NORMAL}Do you want to use Tailwind CSS?{Style.RESET_ALL}", default=True)
    install_drf = click.confirm(f"{Fore.CYAN}{Style.BRIGHT}? {Fore.MAGENTA}{Style.NORMAL}Do you want to install Django REST Framework?{Style.RESET_ALL}", default=False)

    click.echo(f"\n{Fore.GREEN}{Style.BRIGHT}Creating your Django project...{Style.RESET_ALL}")
    
    try:
        from .main import generate_secret_key
        secret_key = generate_secret_key()
        create_project_structure(project_name, app_names, use_tailwind, secret_key, install_drf)  # Tambahkan install_drf
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

@cli.command()
def generate_secret_key():
    """Generate a new secret key for Django."""
    from .main import generate_secret_key
    secret_key = generate_secret_key()
    click.echo(f"{Fore.GREEN}{Style.BRIGHT}Generated Secret Key:{Style.RESET_ALL}")
    click.echo(f"{Fore.YELLOW}{secret_key}{Style.RESET_ALL}")
    click.echo(f"\n{Fore.CYAN}You can use this key in your .env file:{Style.RESET_ALL}")
    click.echo(f"SECRET_KEY={secret_key}")

@cli.command()
def install_drf():
    """Install Django REST Framework and related packages."""
    click.echo(f"{Fore.YELLOW}{Style.BRIGHT}Installing Django REST Framework and related packages...{Style.RESET_ALL}")
    try:
        from .main import install_django_rest_framework
        install_django_rest_framework()
        click.echo(f"{Fore.GREEN}{Style.BRIGHT}Installation completed successfully!{Style.RESET_ALL}")
    except Exception as e:
        click.echo(click.style(f"❌ Installation failed: {str(e)}", fg="red"))

if __name__ == '__main__':
    cli()
