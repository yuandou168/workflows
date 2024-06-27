import requests

class Client():
    def __init__(self, address=None):
        if address is not None:
            self.address = address
        else:
            self.address = "http://127.0.0.1:8000"
            
        self.download_url = self.address + "/download/"
        self.upload_url = self.address + "/upload/"
        self.delete_url = self.address + "/delete/"
        self.metrics_url = self.address + "/metrics/"

        self.session = requests.Session()

    def send_request(self, url, method, file_path):
        try:
            response = method(url, params={"file_path": file_path})
            json = response.json()
            
            if json["success"] == True:
                return True
            else:
                return False
        except Exception as exception:
            return False
    
    def download(self, file_path):
        return self.send_request(self.download_url, self.session.get, file_path)
        
    def upload(self, file_path):
        return self.send_request(self.upload_url, self.session.put, file_path)

    def delete(self, file_path):
        return self.send_request(self.delete_url, self.session.delete, file_path)

    def metrics(self):
        try:
            return self.session.get(self.metrics_url).json()

        except Exception as exception:
            print(exception)
            return None