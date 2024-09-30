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
        if self.user_type == "registered":
            files = self.db.datasite.find() 
        else:
            files = self.db.mockdatasite.find()        

        formatted_files = []
        
        for file in files:
            formatted_file = {
                "name": file.get("name", ""),
                "description": file.get("description", ""),
                "metadata": {
                    "createdBy": file.get("metadata", {}).get("createdBy", ""),
                    "createdAt": {
                        "$numberLong": str(file.get("metadata", {}).get("createdAt", 0))
                    }
                },
                "trainingFiles": [] if self.user_type == "registered" else [],
                "mockFiles": [] if self.user_type == "guest" else []
            }
            
            if self.user_type == "registered":
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
            
            elif self.user_type == "guest":
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


    def download_files(self, file_id: str, download_path: str):
        """
        Description: Download a file
        Parameters: file_id: str, download_path: str
        Creates: File in the download_path
        """
        try:
            file_object_id = ObjectId(file_id)
            file_data = self.fs.find_one({"_id": file_object_id})
            if file_data is None:
                print("Error: File not found")
                Exception("File not found.")
                return None
            directory = os.path.dirname(download_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(download_path, 'wb') as f:
                f.write(self.fs.get(file_data._id).read())
            print(f"File '{file_id}' downloaded successfully to '{download_path}'.")
            return file_data 
        except NoFile:
            print("Error: File not found in GridFS.")
            return None
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None


