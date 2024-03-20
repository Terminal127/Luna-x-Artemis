import paramiko
import logging
import os
import requests
import time
from fuzzywuzzy import process

base_directory = "C:\\Users\\KIIT\\Desktop\\courses"
flask_endpoint = "http://65.0.27.154:8000/get_results"  # Update this with your actual Flask endpoint

def fuzzy_search_files_and_directories(query):
    all_files_and_directories = os.listdir(base_directory)
    matches = process.extractBests(query, all_files_and_directories, score_cutoff=60)

    result = []
    for match in matches:
        item_name = match[0]
        item_path = os.path.join(base_directory, item_name)

        if os.path.isdir(item_path):
            item_type = 'dir'
        else:
            item_type = 'file'

        result.append((item_name, item_type))

    return result

def display_matched_items(matched_items):
    print("Matching items:")
    for item in matched_items:
        item_path = os.path.join(base_directory, item[0])
        if os.path.isdir(item_path):
            print("----- dir", item[0])
        else:
            print(item[0])

def upload_to_ec2(local_file_path, remote_user, remote_instance_ip, remote_destination_path, private_key_path):
    logging.basicConfig(level=logging.INFO)

    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            logging.info(f"Connecting to EC2 instance {remote_instance_ip}...")
            ssh.connect(remote_instance_ip, username=remote_user, key_filename=private_key_path)
            logging.info("Connected successfully!")

            with ssh.open_sftp() as sftp:
                if not os.path.isfile(local_file_path):
                    raise FileNotFoundError(f"Local file not found: {local_file_path}")

                remote_dir = os.path.dirname(remote_destination_path)
                try:
                    sftp.stat(remote_dir)
                except IOError:
                    raise FileNotFoundError(f"Remote directory not found or inaccessible: {remote_dir}")

                logging.info(f"Uploading file '{local_file_path}' to '{remote_destination_path}'...")
                sftp.put(local_file_path, remote_destination_path)
                logging.info("File uploaded successfully!")

    except Exception as e:
        logging.error(f"Error uploading file: {e}")

def send_matched_items(matched_items):
    try:
        # Convert Python data to JSON format
        payload = {'matched_items': matched_items}
        headers = {'Content-Type': 'application/json'}
        
        # Send a POST request to the Flask endpoint
        response = requests.post(flask_endpoint, json=payload, headers=headers)

        if response.status_code == 200:
            print("Matched items sent successfully.")
        else:
            print(f"Failed to send matched items. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error sending matched items: {e}")

def lock_screen_async():
    global base_directory
    directory = "http://65.0.27.154:8000/get_directory_name"
    fuzzurl = "http://65.0.27.154:8000/fuzzy_check"

    while True:
        check = requests.get(fuzzurl)
        if check.status_code == 200:
            json_data = check.json()
            if json_data.get("fuzz_code") == "800":
                search_response = requests.get(directory)
                json_data = search_response.json()
                search_query = json_data.get("dirname")
                print(search_query)
                matched_items = fuzzy_search_files_and_directories(search_query)

                if not matched_items:
                    print("No matches found for the given query.")
                    continue
                
                send_matched_items(matched_items)
                break
            
        
            else:
                print("The code is not set to 800")
        time.sleep(1)
        
if __name__ == "__main__":
    lock_screen_async()
