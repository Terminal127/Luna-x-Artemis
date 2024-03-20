import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/classroom.announcements.readonly"]

def list_announcements(course_id):
    """List announcements for a given course."""
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("classroom", "v1", credentials=creds)

        # Call the Classroom API
        response = service.courses().announcements().list(
            courseId=course_id,
            announcementStates=["PUBLISHED"],
            orderBy="updateTime",
            pageSize=10  # You can adjust this based on your needs
        ).execute()

        return response

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def save_announcements_to_file(announcements, filename="announcements_response.json"):
    """Save the formatted JSON response containing announcements to a file."""
    if announcements:
        with open(filename, "w") as file:
            json.dump(announcements, file, indent=2)
        print(f"Announcements response saved to {filename}")
    else:
        print("No announcements response to save.")

if __name__ == "__main__":
    # Replace 'your_course_id' with the actual Course ID you want to retrieve announcements for
    course_id = '651105789018'
    announcements_response = list_announcements(course_id)
    save_announcements_to_file(announcements_response)
