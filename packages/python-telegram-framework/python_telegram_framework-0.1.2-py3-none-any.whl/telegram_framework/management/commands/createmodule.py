import os
import sys

from telegram_framework.conf import settings
from telegram_framework.management.base import CommandError
from telegram_framework.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = "Create a new module within the project"
    template_name = "module_template"
    
    def __init__(self, argv):
        super().__init__(argv)
        
    def ask_include_handlers(self, module_name):
        include_handlers = input("Do you want to include the handlers of this new module in the app handlers? (y/n):").strip().lower()
        if include_handlers == "y":
            app_handlers_path = os.path.join('app', 'handlers.py')
            module_import = f"*include('{module_name}.handlers')"
            include_import = "from telegram_framework.handlers import include"
            
            try:
                with open(app_handlers_path, 'r') as f:
                    content = f.readlines()
            except FileNotFoundError:
                print(f"The file '{app_handlers_path}' does not exist.")
                sys.exit(1)

            include_import_exists = any(include_import in line for line in content)
            module_import_exists = any(module_import in line for line in content)
            
            try:
                with open(app_handlers_path, 'w') as f:
                    count = 0
                    for line in content:
                        # Import the 'include' function at the beginning of the file, if it has not already been imported
                        if count == 0 and not include_import_exists:
                            f.write(f"{include_import}\n")
                        # Write next line in file
                        f.write(line)
                        # Add 'include' function at the begining of the handlers list
                        if not module_import_exists and line.strip().startswith("handlers = ["):
                            f.write(f"\t{module_import},\n")
                            
                        count += 1
                
                print(f"Handlers of module '{module_name}' included in app handlers successfully.")
                # reverse = input("\nDo you want to reverse the action? (y/n):").strip().lower()
                # if reverse == "y":
                #     with open(app_handlers_path, 'w') as f:
                #         f.writelines(content)
                #     print("Action successfully reversed.")
            except Exception as e:
                print(f"Error while including handlers: {e}")
                with open(app_handlers_path, 'w') as f:
                    f.writelines(content)
                sys.exit(1)

    def handle(self, **options):
        name = options.get('name')

        base_directory = os.path.join(os.getcwd(), *settings.MODULES_DIR.split('.'))
        destination = os.path.join(base_directory, name)
        self.copy_template(destination)
        
        print(f"Module '{name}' created successfully at {destination}\n")
        
        self.ask_include_handlers(name)
        
