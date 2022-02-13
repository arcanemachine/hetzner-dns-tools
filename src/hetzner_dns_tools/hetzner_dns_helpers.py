import requests
import sys


def check_response_for_errors(response_dict):
    """
    Check a response dictionary for errors.

    If an error is found:
        - In Bash: Print error to the console and exit with error code 1
        - In Python: Raise a ValueError exception
    """
    if response_dict.get('error') or response_dict.get('message'):
        error_message = ""
        if response_dict.get('error'):
            error_message = response_dict['error']['message']
        elif response_dict.get('message'):
            error_message = response_dict['message']

        if __name__ == '__main__':
            print(f"Error: {error_message}")
            sys.exit(1)  # exit with error
        else:
            raise ValueError(error_message)


def exit_with_error(error_message, exception_type=ValueError):
    """A boilerplate function to exit the program with an error message."""
    if __name__ == '__main__':
        print(f"Error: {error_message}")
        sys.exit(1)  # exit with error
    else:
        raise exception_type(error_message)


def handle_request_exception(err):
    """A boilerplate function for handling request exceptions."""
    # when running via the terminal, print output to console then exit
    if __name__ == '__main__':
        print(f"Error: {err}")
        sys.exit(1)  # exit with error
    else:
        raise requests.exceptions.RequestException(err)
