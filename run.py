import os
import argparse
import requests

# URL for the web service open-hrv API endpoint
URL = 'https://hrvwebapi-flask-76wlsdg7yq-lm.a.run.app/calculate'


def parse_args():
    """Parses command-line arguments and performs basic validation.

    Returns:
        argparse.Namespace: An object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Send data to a specific endpoint with form-data.")
    parser.add_argument('-f', '--file', required=True, type=argparse.FileType('rb'), help="Path to the data file (binary format).")
    parser.add_argument('-s', '--sampling-rate', required=True, type=int, help="Sampling rate of the data (in Hz).")
    parser.add_argument('-d', '--data-type', required=True, choices=['PPG', 'ECG', 'RRS'], help="Type of data (PPG, ECG, or RRS).")

    args = parser.parse_args()

    # Validate file argument
    if not args.file.name.endswith(('.bin', '.dat', '.csv')):
        raise argparse.ArgumentError('-f: File extension must be .bin or .dat.')

    return args

def send_request(endpoint, file_path, sampling_rate, data_type):
    """Sends a request to the specified endpoint with form-data containing the file, sampling rate, and data type.

    Args:
        endpoint (str): URL of the endpoint.
        file_data (bytes): Content of the data file.
        sampling_rate (int): Sampling rate of the data.
        data_type (str): Type of data (PPG, ECG, or RRS).

    Returns:
        requests.Response: The HTTP response object.
    """
    current_dir = os.getcwd()
    files = {
        'file': open(os.path.join(current_dir, file_path), 'rb'),
    }   
    data = {'sampling_rate': sampling_rate, 'data_type': data_type}
    
    try:
        response = requests.post(endpoint, files=files, data=data)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        return response
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error sending request: {e}")

def main():
    args = parse_args()
    endpoint = URL
    file_path = str(args.file.name)
    sampling_rate = args.sampling_rate
    data_type = args.data_type

    try:
        response = send_request(endpoint, file_path, sampling_rate, data_type)
        print(f"Request sent successfully. Response status code: {response.status_code}")
        print(f"Response content your HRV: {response.content}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
