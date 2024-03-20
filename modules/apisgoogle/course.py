import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me.readonly"
]

def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Read course IDs and names from the file
        with open("course_ids.json", "r") as course_file:
            course_data = json.load(course_file)

        for course_info in course_data:
            course_id = course_info.get("id", "No ID")
            course_name = course_info.get("name", "No Name")

            service = build("classroom", "v1", credentials=creds)

            # Request only the necessary fields for course work
            course_work = service.courses().courseWork().list(
                courseId=course_id,
                courseWorkStates=["PUBLISHED"],
                orderBy="dueDate asc"  # You can adjust sorting as needed
            ).execute()

            # Check if there is no course work
            if not course_work.get('courseWork'):
                print(f"No course work available for course ID {course_id} - {course_name}.")
                continue

            # Iterate through course work items
            for work_item in course_work.get('courseWork', []):
                due_date = work_item.get('dueDate', 'No due date')
                if due_date != 'No due date':
                    # Format due date if available
                    due_date = due_date.strftime("%Y-%m-%d %H:%M:%S")
                print(f"Course ID: {course_id}")
                print(f"Course Name: {course_name}")
                print(f"Course Work Title: {work_item['title']}")
                print(f"Due Date: {due_date}")
                print(f"Status: {work_item['state']}")
                print("-" * 30)

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
