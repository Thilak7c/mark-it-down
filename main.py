from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from markitdown import MarkItDown
import tempfile
import os

app = FastAPI()

# Enable CORS so your Vercel frontend can call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

md = MarkItDown()

@app.get("/")
def home():
    return {"status": "MarkItDown API is running!"}

@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Convert to Markdown using MarkItDown
        result = md.convert(tmp_path)

        # Cleanup temp file
        os.remove(tmp_path)

        return {"filename": file.filename, "markdown": result.text_content}
    except Exception as e:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))
