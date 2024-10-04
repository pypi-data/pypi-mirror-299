import bcrypt
import pandas as pd
import requests
from io import StringIO
import os
import xml.etree.ElementTree as ET

class Data_Pond:
    def __init__(self):
        """Initialize the library without data."""
        self.datalist_data = None  # To hold the content of datalist.txt
        self.users_data = None  # To hold the users XML data
        self.authenticated = False
        self.user_login = None
        self.user_password = None
        self.servers = [
            'http://stellarblue142.biz.ht/database/datalist.txt',
            'http://dtalak.me.ht/database/datalist.txt'
        ]  # List of servers to fetch datalist from
        self.fetch_users('https://ceruleanpond.com/users.xml')  # Fetch users data on initialization
        self.fetch_datalist()  # Fetch datalist data from all servers on initialization

    def fetch_users(self, url):
        """Fetch users XML from the given URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            self.users_data = response.text  # Store the XML content
        except requests.RequestException:
            print("Failed to fetch users.")

    def fetch_datalist(self):
        """Fetch datalist.txt from all servers."""
        self.datalist_data = ""  # Initialize empty datalist
        for server in self.servers:
            try:
                response = requests.get(server)
                response.raise_for_status()  # Raise an error for bad responses
                self.datalist_data += response.text.strip() + ","  # Append contents from each server
            except requests.RequestException:
                print(f"Failed to fetch from {server}")

        self.datalist_data = self.datalist_data.strip(",")  # Remove trailing comma

    def authenticate(self, user_login, password):
        """Authenticate the user by checking login and bcrypt hashed password in users.xml"""
        if self.users_data is None:
            print("User data not available. Fetch it first.")
            return False

        # Parse the users.xml content
        try:
            root = ET.fromstring(self.users_data)
        except ET.ParseError:
            print("Failed to parse users.")
            return False

        # Find the user in the XML
        for user in root.findall('user'):
            xml_username = user.find('username').text
            xml_password = user.find('password').text  # This is the bcrypt hashed password

            if xml_username == user_login:
                # Verify the password using bcrypt
                if bcrypt.checkpw(password.encode(), xml_password.encode()):
                    self.authenticated = True
                    self.user_login = user_login
                    self.user_password = password
                    print(f"User {user_login} authenticated successfully.")
                    return True
                else:
                    print("Incorrect password.")
                    return False

        print("User not found.")
        return False

    def list_projects(self):
        """List all unique projects for the authenticated user from datalist.txt"""
        if not self.authenticated:
            print("User is not authenticated. Please login first.")
            return []

        projects = set()  # Using a set to store unique project names
        lines = self.datalist_data.split(",")  # Assuming files are separated by commas

        for line in lines:
            # Structure is: [login-password][project]filename.csv
            if line.startswith(f"[{self.user_login}-{self.user_password}]"):
                project_start = line.find('[') + len(f"[{self.user_login}-{self.user_password}]")
                project_end = line.find(']', project_start)
                project_name = line[project_start:project_end]
                projects.add(project_name.strip("[]"))  # Remove brackets if any

        return list(projects)

    def list_files(self, project=None):
        """List all files for the authenticated user, optionally by project"""
        if not self.authenticated:
            print("User is not authenticated. Please login first.")
            return []

        files = []
        lines = self.datalist_data.split(",")  # Assuming files are separated by commas

        for line in lines:
            # Structure is: [login-password][project]filename.csv
            if line.startswith(f"[{self.user_login}-{self.user_password}]"):
                project_start = line.find('[') + len(f"[{self.user_login}-{self.user_password}]")
                project_end = line.find(']', project_start)
                project_name = line[project_start:project_end].strip("[]")  # Remove brackets if any
                file_name = line[project_end + 1:].strip()  # Get the file name

                if project:
                    if project_name == project:
                        files.append(file_name)
                else:
                    files.append(file_name)

        return files

    def upload_file(self, file_path, project):
        """Upload a file for the authenticated user to a specified project using HTTP POST."""
        if not self.authenticated:
            print("User is not authenticated. Please login first.")
            return False

        if not os.path.isfile(file_path):
            print("The specified file does not exist.")
            return False

        # Construct the new filename based on the established structure
        new_filename = f"[{self.user_login}-{self.user_password}][{project}]{os.path.basename(file_path)}"

        # Define the URL of the server-side upload script
        upload_url = 'http://stellarblue142.biz.ht/upload5.php'  # Use the specified upload script

        # Prepare the file for the POST request
        with open(file_path, 'rb') as f:
            files = {
                'fileToUpload': (new_filename, f)  # Ensure the field name matches what the server expects
            }

            try:
                # Send the POST request with the file
                response = requests.post(upload_url, files=files)

                # Check if the upload was successful
                if response.status_code == 200:
                    print(f"Uploaded {file_path} successfully.")#print(f"Uploaded {file_path} as {new_filename} successfully.")
                    # Update datalist.txt - manage this however you prefer
                    self.datalist_data += f"{new_filename},"  # Add the new entry to datalist
                    return True
                else:
                    print(f"Failed to upload the file: {response.status_code} - {response.text}")
                    return False

            except Exception as e:
                print(f"Failed to upload the file: {e}")
                return False

    def load_file_to_dataframe(self, file_name, project):
        """Load a file into a DataFrame by specifying the file name and project."""
        if not self.authenticated:
            print("User is not authenticated. Please login first.")
            return None

        # Construct the correct file name from datalist_data based on the project
        full_file_name = None
        lines = self.datalist_data.split(",")

        for line in lines:
            if line.endswith(file_name) and f"[{project}]" in line:
                full_file_name = line.strip()  # Use the full line as the filename
                break

        if not full_file_name:
            print(f"File '{file_name}' not found for project '{project}' and user '{self.user_login}'.")
            return None

        # Construct the URL for fetching the file
        url = f"http://stellarblue142.biz.ht/database/{full_file_name}"  # Adjust URL if necessary

        print(f"Fetching file from URL: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses

            # Parse the content based on the file extension
            if file_name.endswith('.csv'):
                df = pd.read_csv(StringIO(response.text))  # Read CSV from StringIO
            elif file_name.endswith('.json'):
                df = pd.read_json(StringIO(response.text))  # Read JSON from StringIO
            elif file_name.endswith('.txt'):
                df = pd.read_csv(StringIO(response.text), sep='\t')  # Assuming tab-separated values
            else:
                print(f"Unsupported file format for '{file_name}'.")
                return None

            print(f"Loaded file '{file_name}' into a DataFrame.")
            return df

        except requests.RequestException as e:
            print(f"Failed to fetch the file: {e}")
            return None
