from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import zipfile
from pathlib import Path
import os
import sys
import subprocess
import shutil

# 🔥 FIX IMPORT PATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

# ✅ IMPORT PCB FUNCTION
from api.main import generate_pcb_from_params

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MODELS
# =========================
class PCBRequest(BaseModel):
    width: float
    height: float


class PromptRequest(BaseModel):
    prompt: str


# =========================
# PATHS
# =========================
OUTPUT_DIR = Path("generated_files")
OUTPUT_DIR.mkdir(exist_ok=True)

# 👉 Existing PCB files
EXISTING_OUTPUT_DIR = Path(r"D:\El-Maze\2026\output")


# =========================
# EXISTING ENDPOINT (UNCHANGED)
# =========================
@app.post("/api/generate-pcb")
async def generate_pcb(data: PCBRequest):
    try:
        folder_id = str(uuid.uuid4())
        pcb_folder = OUTPUT_DIR / folder_id
        pcb_folder.mkdir(parents=True, exist_ok=True)

        generate_pcb_from_params(pcb_folder, data.width, data.height)

        zip_path = pcb_folder.with_suffix(".zip")

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in pcb_folder.glob("*"):
                zipf.write(file, file.name)

        return FileResponse(
            path=zip_path,
            filename="pcb_gerber.zip",
            media_type="application/zip"
        )

    except Exception as e:
        return {"error": str(e)}


# =========================
# PROMPT → OLLAMA + FILE
# =========================
@app.post("/api/generate-from-prompt")
async def generate_from_prompt(data: PromptRequest):
    try:
        prompt = data.prompt
        print("User Prompt:", prompt)

        # =========================
        # 🧠 OLLAMA RESPONSE (qwen)
        # =========================
        try:
            result = subprocess.run(
                ["ollama", "run", "qwen3.5:4b", prompt],
                capture_output=True,
                text=True,
            )
            ollama_output = result.stdout.strip()
        except Exception as e:
            ollama_output = f"Ollama failed: {str(e)}"

        print("Ollama Output:", ollama_output)

        # =========================
        # 🔍 GET FILE FROM OUTPUT
        # =========================
        if not EXISTING_OUTPUT_DIR.exists():
            return {"error": "Output folder not found"}

        files = list(EXISTING_OUTPUT_DIR.glob("*"))

        if not files:
            return {"error": "No files found in output folder"}

        latest_file = max(files, key=os.path.getmtime)
        print("Selected file:", latest_file)

        # =========================
        # 📁 COPY FILE TO TEMP
        # =========================
        file_id = str(uuid.uuid4())
        temp_file = OUTPUT_DIR / f"{file_id}_{latest_file.name}"

        shutil.copy(latest_file, temp_file)

        # =========================
        # 🔗 DOWNLOAD URL
        # =========================
        download_url = f"http://localhost:8000/api/download/{temp_file.name}"

        return JSONResponse({
            "message": ollama_output,
            "file_url": download_url,
            "file_name": latest_file.name
        })

    except Exception as e:
        return {"error": str(e)}


# =========================
# DOWNLOAD ENDPOINT
# =========================
@app.get("/api/download/{filename}")
async def download_file(filename: str):
    file_path = OUTPUT_DIR / filename

    if not file_path.exists():
        return {"error": "File not found"}

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )