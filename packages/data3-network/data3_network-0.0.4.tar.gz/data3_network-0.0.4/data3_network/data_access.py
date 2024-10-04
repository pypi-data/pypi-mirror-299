import os
from pymongo import MongoClient
from gridfs import GridFS, NoFile
import datetime
from bson.objectid import ObjectId

class DataAccess:
    """
    :Description: Data Access class for interacting with data
    :Attributes: ip: str, username: str, password: str
    :Method view_files: view all files
    :Method download_files: download a file
    """

    def __init__(self, ip: str, username: str = None, password: str = None):
        self.mongo_client = self._connect_to_database(ip, username, password)
        self.db = self.mongo_client['datasite'] if username and password else self.mongo_client['mockdatasite']
        self.fs = GridFS(self.db)
        self.user_type = "registered" if username and password else "guest"

        # Setting up guest client for mockdatasite (always used for fetching mock data)
        self.guest_client = MongoClient(f"mongodb://guest:data3network@{ip}:27017/mockdatasite")
        self.guest_db = self.guest_client['mockdatasite']
        self.guest_fs = GridFS(self.guest_db)  # Separate GridFS instance for mock data

    def _connect_to_database(self, ip: str, username: str = None, password: str = None):
        if username and password:
            uri = f"mongodb://{username}:{password}@{ip}:27017/datasite"
        else:
            uri = f"mongodb://guest:data3network@{ip}:27017/mockdatasite"

        try:
            client = MongoClient(uri)
            print("Connected to MongoDB successfully.")
            return client
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return None

    def view_files(self):
        """
        Description: View all files in the database
        Parameters: None
        Returns: List of file metadata
        """
        formatted_files = []

        # Fetch training files from the 'datasite' collection (for registered users)
        if self.user_type == "registered":
            training_files_cursor = self.db.datasite.find()
            for file in training_files_cursor:
                formatted_file = {
                    "name": file.get("name", ""),
                    "description": file.get("description", ""),
                    "metadata": {
                        "createdBy": file.get("metadata", {}).get("createdBy", ""),
                        "createdAt": {
                            "$numberLong": str(file.get("metadata", {}).get("createdAt", 0))
                        }
                    },
                    "trainingFiles": [],
                    "mockFiles": []
                }
                
                for training_file in file.get("trainingFiles", []):
                    formatted_training_file = {
                        "fileName": training_file.get("fileName", ""),
                        "uploadedAt": {
                            "$date": training_file.get("uploadedAt", "").isoformat() if isinstance(training_file.get("uploadedAt"), datetime.datetime) else ""
                        },
                        "fileId": training_file.get("fileId", ""),
                        "fileSize": {
                            "$numberLong": str(training_file.get("fileSize", 0))
                        }
                    }
                    formatted_file["trainingFiles"].append(formatted_training_file)
                
                formatted_files.append(formatted_file)

        # Fetch mock files from the 'mockdatasite' collection (use guest logic even for registered users)
        mock_files_cursor = self.guest_db.mockdatasite.find()
        for file in mock_files_cursor:
            formatted_file = {
                "name": file.get("name", ""),
                "description": file.get("description", ""),
                "metadata": {
                    "createdBy": file.get("metadata", {}).get("createdBy", ""),
                    "createdAt": {
                        "$numberLong": str(file.get("metadata", {}).get("createdAt", 0))
                    }
                },
                "trainingFiles": [],
                "mockFiles": []
            }
            
            for mock_file in file.get("mockFiles", []):
                formatted_mock_file = {
                    "fileName": mock_file.get("fileName", ""),
                    "uploadedAt": {
                        "$date": mock_file.get("uploadedAt", "").isoformat() if isinstance(mock_file.get("uploadedAt"), datetime.datetime) else ""
                    },
                    "fileId": mock_file.get("fileId", ""),
                    "fileSize": {
                        "$numberLong": str(mock_file.get("fileSize", 0))
                    }
                }
                formatted_file["mockFiles"].append(formatted_mock_file)
            
            formatted_files.append(formatted_file)
        
        return formatted_files

    def _download_single_file(self, file, is_mock=False):
        file_id = file.get("fileId")
        file_name = file.get("fileName")
        
        if file_id is None:
            print(f"Error: No file_id found for the file '{file_name}'. Skipping download.")
            return

        # Convert file_id to ObjectId for GridFS lookup
        try:
            file_id = ObjectId(file_id)
        except Exception as e:
            print(f"Error converting file_id to ObjectId: {e}")
            return

        download_dir = os.path.join("download", str(file_id))

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        download_path = os.path.join(download_dir, file_name)

        # Check if the file already exists
        if os.path.exists(download_path):
            print(f"File '{file_name}' already exists in '{download_dir}'.")
            return

        # Download file if it doesn't exist
        try:
            fs_instance = self.guest_fs if is_mock else self.fs
            with open(download_path, 'wb') as f:
                f.write(fs_instance.get(file_id).read())
            print(f"File '{file_name}' downloaded successfully to '{download_path}'.")
        except NoFile:
            print(f"Error: File '{file_name}' not found in GridFS.")
        except Exception as e:
            print(f"Error downloading file '{file_name}': {e}")

    def download_files(self, file_type: str, file_names: list = []):
        """
        Description: Download a file or multiple files (training/mock/all)
        Parameters: 
            file_type: str ("training", "mock", or "all")
            file_names: list (specific filenames to download, empty list means download all)
        Creates: Files in the "download/<file_id>/<file_name>" path
        """
        if self.user_type == "guest" and file_type in ["training", "all"]:
            print("Guest users cannot download training files.")
            return None
        
        # Fetch all files based on type
        training_files = []
        mock_files = []
        if file_type in ["training", "all"]:
            training_files = self.db.datasite.find() if self.user_type == "registered" else []
        if file_type in ["mock", "all"]:
            mock_files = self.guest_db.mockdatasite.find()

        files_to_download = []

        # If specific file names are provided, fetch those
# Filter files based on provided file names or download all
        if file_names:
            if file_type in ["training", "all"]:
                files_to_download.extend([file for file in training_files if any(tf['fileName'] in file_names for tf in file.get('trainingFiles', []))])
            if file_type in ["mock", "all"]:
                files_to_download.extend([file for file in mock_files if any(mf['fileName'] in file_names for mf in file.get('mockFiles', []))])
        else:
            if file_type in ["training", "all"]:
                files_to_download.extend(training_files)
            if file_type in ["mock", "all"]:
                files_to_download.extend(mock_files)

        print(f"Files to download: {files_to_download}")  # Debugging statement

        # Process download
        for file in files_to_download:
            # Handle mock files
            if (file_type == "mock" or file_type == "all") and "mockFiles" in file:
                for mock_file in file.get("mockFiles", []):
                    self._download_single_file(mock_file, is_mock=True)
            
            # Handle training files
            if (file_type == "training" or file_type == "all") and "trainingFiles" in file:
                for training_file in file.get("trainingFiles", []):
                    self._download_single_file(training_file, is_mock=False)