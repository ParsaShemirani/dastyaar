from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    with open('/Users/parsashemirani/Main/fakeintake/WICKEDUP.txt', 'wb') as f:
        f.write(contents)
    return {"ok": True, "filename": file.filename, "size": len(contents)}
