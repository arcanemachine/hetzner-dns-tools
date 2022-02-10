import requests
import sys


def check_response_for_errors(response_dict):
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


def handle_request_exception(err):
    # when running via the terminal, print output to console then exit
    if __name__ == '__main__':
        print(f"Error: {err}")
        sys.exit(1)  # exit with error
    else:
        raise requests.exceptions.RequestException(err)
