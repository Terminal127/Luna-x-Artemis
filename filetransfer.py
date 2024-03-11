import paramiko
import logging
import os
import requests
import time

def upload_to_ec2(local_file_path, remote_user, remote_instance_ip, remote_destination_path, private_key_path):
  """
  Uploads a file to a remote EC2 instance using SFTP with paramiko.

  Args:
      local_file_path (str): Path to the local file to upload.
      remote_user (str): Username on the remote EC2 instance.
      remote_instance_ip (str): IP address of the remote EC2 instance.
      remote_destination_path (str): Path on the remote EC2 instance to store the uploaded file.
      private_key_path (str): Path to the private key file for authentication.

  Returns:
      None
  """

  logging.basicConfig(level=logging.INFO)

  try:
    # Create SSH client with AutoAddPolicy for missing host keys
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to EC2 instance using username, IP, and private key
    logging.info(f"Connecting to EC2 instance {remote_instance_ip}...")
    ssh.connect(remote_instance_ip, username=remote_user, key_filename=private_key_path)
    logging.info("Connected successfully!")

    # Open SFTP session
    sftp = ssh.open_sftp()

    # Verify local file exists and remote directory has write permissions
    if not os.path.isfile(local_file_path):
      raise Exception(f"Local file not found: {local_file_path}")

    remote_dir = os.path.dirname(remote_destination_path)  # Extract remote directory
    try:
      sftp.stat(remote_dir)  # Check if remote directory exists
    except IOError:
      raise Exception(f"Remote directory not found or inaccessible: {remote_dir}")

    # Upload the file
    logging.info(f"Uploading file '{local_file_path}' to '{remote_destination_path}'...")
    sftp.put(local_file_path, remote_destination_path)
    logging.info("File uploaded successfully!")

  except Exception as e:
    logging.error("Error uploading file:", exc_info=True)  # Log full exception details
  finally:
    # Close SFTP and SSH connections
    if sftp:
      sftp.close()
    if ssh:
      ssh.close()

# Example usage (replace with your actual values)
local_file_path = "C:\\Users\\KIIT\\Desktop\\courses\\ai\\mad\\RealtimeTTS\\README.md"
remote_user = "ubuntu"
remote_instance_ip = "3.109.54.85"
remote_destination_path = "/home/ubuntu/README.md"
private_key_path = "C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna\\New-keypair.pem"

def lock_screen_async():
    while True:
        try:
            url = "http://3.109.54.85:8080/lock"
            response = requests.get(url)

            if response.status_code == 200:
                json_data = response.json()
                if json_data.get("lock_code") == "201":
                    upload_to_ec2(local_file_path, remote_user, remote_instance_ip, remote_destination_path, private_key_path)
                    break

                else:
                    print("the code is not 201. file couldnt be sent")
                    
            else:
                 print("other than 200 status code received from the server. file couldnt be sent")
        except Exception as e:
            print(f"Error sending lock request: {e}")
        time.sleep(1)

if __name__=="__main__":
        lock_screen_async()

