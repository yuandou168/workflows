import uvicorn
import os
from fastapi import FastAPI
from service import Service

service = Service()
app = FastAPI()

@app.get("/download/")
def download(file_path : str):
    if os.path.isfile(file_path):
        return {"success": True, "message": None}
        
    status, message = service.download(file_path)

    return {"success": status, "message": message}

@app.put("/upload/")
def upload(file_path : str):
    status, message = service.upload(file_path)

    return {"success": status, "message": message}

@app.delete("/delete/")
def delete(file_path: str):
    status, message = service.delete(file_path)

    return {"success": status, "message": message}

@app.get("/metrics/")
def metrics():
    return service.metrics()

if __name__ == "__main__":
    bind_address = "0.0.0.0"
    if os.environ.get("BIND_ADDRESS") != None:
        bind_address = os.environ["BIND_ADDRESS"]

    uvicorn.run(app, host=bind_address, port=8000, log_level="info")