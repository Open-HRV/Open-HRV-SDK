import os
import argparse
import requests

# URL for the web service open-hrv API endpoint
URL = 'https://hrvwebapi-flask-76wlsdg7yq-lm.a.run.app/calculate'
URL_SEGMENTS = 'https://hrvwebapi-flask-76wlsdg7yq-lm.a.run.app/calculate_with_epoch'


def parse_args():
    """Parses command-line arguments and performs basic validation.

    Returns:
        argparse.Namespace: An object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Send data to a specific endpoint with form-data.")
    parser.add_argument('-f', '--file', required=True, type=argparse.FileType('rb'), help="Path to the data file (binary format).")
    parser.add_argument('-s', '--sampling-rate', required=True, type=int, help="Sampling rate of the data (in Hz).")
    parser.add_argument('-d', '--data-type', required=True, choices=['PPG', 'ECG', 'RRS'], help="Type of data (PPG, ECG, or RRS).")
    parser.add_argument('-sg', '--segments', action='store_true', help="If specified, the data should be segmented")
    parser.add_argument('-l', '--segment-length', type=int, help="Length of each segment (in seconds).")
    parser.add_argument('-o', '--overlap', type=float, help="Overlap between segments form 0 to 1.")

    args = parser.parse_args()

    # Validate file argument
    if not args.file.name.endswith(('.bin', '.dat', '.csv')):
        raise argparse.ArgumentError('-f: File extension must be .bin or .dat.')

    return args

def send_single_request(endpoint, file_path, sampling_rate, data_type):
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

def send_segmented_request(endpoint, file_path, sampling_rate, data_type, segment_length, overlap):
    """Sends a request to the specified endpoint with form-data containing the file, sampling rate, and data type.

    Args:
        endpoint (str): URL of the endpoint.
        file_data (bytes): Content of the data file.
        sampling_rate (int): Sampling rate of the data.
        data_type (str): Type of data (PPG, ECG, or RRS).
        segment_length (int): Length of each segment (in seconds).
        overlap (float): Overlap between segments form 0 to 1.

    Returns:
        requests.Response: The HTTP response object.
    """
    current_dir = os.getcwd()
    files = {
        'file': open(os.path.join(current_dir, file_path), 'rb'),
    }   
    data = {'sampling_rate': sampling_rate, 'data_type': data_type, 'segment_length': segment_length, 'segment_overlap': overlap}
    print(data)
    try:
        response = requests.post(endpoint, files=files, data=data)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        return response
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error sending request: {e}")

def main():
    args = parse_args()
    file_path = str(args.file.name)
    sampling_rate = args.sampling_rate
    data_type = args.data_type
    segments = args.segments
    segment_length = args.segment_length
    overlap = args.overlap

    try:
        if segments:
            response = send_segmented_request(URL_SEGMENTS, file_path, sampling_rate, data_type, segment_length, overlap)
        else:
            response = send_single_request(URL, file_path, sampling_rate, data_type)
        print(f"Request sent successfully. Response status code: {response.status_code}")
        print(f"Response content your HRV: {response.content}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
