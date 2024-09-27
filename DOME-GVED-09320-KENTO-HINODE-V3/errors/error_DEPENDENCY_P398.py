import subprocess
import re
import logging

def handle_dependency_error(error_message):
    """Handles the P398 dependency error by installing missing libraries."""
    try:
        # Extract missing library names from the error message
        missing_libraries = re.findall(r"'([^']*)'", error_message)
        
        if missing_libraries:
            print("The following libraries are missing and will be installed:")
            for lib in missing_libraries:
                print(f"- {lib}")

            # Install missing libraries
            for lib in missing_libraries:
                subprocess.check_call(["pip", "install", lib])
                logging.info(f"Installed missing library: {lib}")

            return True  # Indicate successful installation
        else:
            logging.error("Could not identify missing libraries from error message.")
            return False

    except Exception as e:
        logging.error(f"Error installing dependencies: {e}")
        return False