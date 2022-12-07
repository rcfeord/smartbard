import uvicorn
from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from smartbard import be_smart_be_bard

app = FastAPI()
dir = Path(Path.cwd().parent, 'img_tmp')

# Define a root `/` endpoint
@app.get('/')
def index():
    return {'OK': 'Welcome to SmartBard API'}

# Generate endpoint
@app.post("/generate")
def get_image(upload_file: UploadFile = File(...)):

    def make_tmp_file(upload_file: UploadFile) -> Path:
        try:
            suffix = Path(upload_file.filename).suffix
            with NamedTemporaryFile(delete=False, suffix=suffix, dir=dir) as tmp:
                shutil.copyfileobj(upload_file.file, tmp)
                tmp_path = Path(tmp.name)
        finally:
            upload_file.file.close()

        return tmp_path

    img_path = make_tmp_file(upload_file)

    final_limerick = be_smart_be_bard(img_path)

    img_path.unlink()

    return {"limerick": final_limerick}

    # return {"path": img_path}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
