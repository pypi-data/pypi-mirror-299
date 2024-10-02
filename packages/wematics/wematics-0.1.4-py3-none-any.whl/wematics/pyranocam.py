import requests
import os
import re
import datetime
from tqdm import tqdm
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo


import requests
import os
import re
import datetime
from tqdm import tqdm
from zoneinfo import ZoneInfo

class Pyranocam:
    def __init__(self, api_key):
        self.base_url = "http://wematics.cloud"
        self.api_key = api_key

    def _make_request(self, endpoint: str, params=None):
        """Makes a request to the API with error handling."""
        url = f"{self.base_url}{endpoint}"
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        print(url)
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def list_cameras(self):
        """Lists all available cameras for the user."""
        return self._make_request("/cameras")

    def list_variables(self, camera):
        """Lists all available variables for a given camera."""
        return self._make_request(f"/{camera}/variables")

    def list_dates(self, camera, variable):
        """Lists all available dates for a given camera and variable."""
        return self._make_request(f"/{camera}/dates/{variable}")

    def list_files(self, camera, variable, date, timezone='local'):
        """Lists all available files for a given camera, variable, and date."""
        params = {'timezone': timezone}
        return self._make_request(f"/{camera}/files/{variable}/{date}", params)

    def download_file(self, camera, variable, file_name, download_path="", timezone='local'):
        """Downloads a single file."""
        params = {'timezone': timezone}
        url = f"{self.base_url}/{camera}/download/{variable}/{file_name}"
        self._download_file(url, os.path.basename(file_name), download_path, params)

    def _download_file(self, url, file_name, download_path="", params=None):
        """Downloads a file from a given URL (helper function)."""
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        response = requests.get(url, params=params, stream=True)

        if response.status_code == 200:
            file_path = os.path.join(download_path, file_name)
            total_size = int(response.headers.get('content-length', 0))

            with open(file_path, 'wb') as f:
                for chunk in tqdm(response.iter_content(chunk_size=4096), 
                                total=total_size // 4096, 
                                unit='KB', 
                                desc=f"Downloading {file_name}"):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Error downloading {file_name}: {response.text}")



    def download_files_in_range(self, camera, variable, start_datetime, end_datetime, download_path=".", timezone='local'):
        """Downloads files for a camera and variable within a datetime range with a progress bar."""
        
        # Extract date parts using regex
        start_match = re.search(r"(\d{4}-\d{2}-\d{2})", start_datetime)
        end_match = re.search(r"(\d{4}-\d{2}-\d{2})", end_datetime)
        
        if not start_match or not end_match:
            raise ValueError("Invalid datetime format. Expected YYYY-MM-DD in start_datetime and end_datetime.")
        
        start_date = datetime.datetime.strptime(start_match.group(1), "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_match.group(1), "%Y-%m-%d").date()
        
        all_files = []
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            files = self.list_files(camera, variable, date_str, timezone)['files']
            all_files.extend(files)
            current_date += datetime.timedelta(days=1)
        
        filtered_files = []
        start_dt = datetime.datetime.strptime(re.search(r"(\d{4}-\d{2}-\d{2}_\d{2}_\d{2}_\d{2})", start_datetime).group(1), "%Y-%m-%d_%H_%M_%S")
        end_dt = datetime.datetime.strptime(re.search(r"(\d{4}-\d{2}-\d{2}_\d{2}_\d{2}_\d{2})", end_datetime).group(1), "%Y-%m-%d_%H_%M_%S")

        for file_name in all_files:
            match = re.search(r"(\d{4}-\d{2}-\d{2}_\d{2}_\d{2}_\d{2})", file_name)
            if match:
                file_dt = datetime.datetime.strptime(match.group(1), "%Y-%m-%d_%H_%M_%S")
                if start_dt <= file_dt < end_dt:
                    filtered_files.append(file_name)
                    
        if not filtered_files:
            for file_name in all_files:
                match = re.search(r"(\d{4}-\d{2}-\d{2})", file_name)
                if match:
                    file_dt = datetime.datetime.strptime(match.group(1), "%Y-%m-%d")
                    filtered_files.append(file_name)
                    
        for file_name in tqdm(filtered_files, desc="Downloading", unit="file"):
            self.download_file(camera, variable, file_name, download_path, timezone)