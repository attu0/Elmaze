from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import zipfile
from pathlib import Path
import os
import sys
import subprocess

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

# 👉 Your existing PCB output folder
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

        # 🔥 GENERATE PCB
        generate_pcb_from_params(pcb_folder, data.width, data.height)

        # 📦 ZIP FILES
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
# NEW PROMPT ENDPOINT
# =========================
@app.post("/api/generate-from-prompt")
async def generate_from_prompt(data: PromptRequest):
    try:
        prompt = data.prompt

        print("User Prompt:", prompt)

        # 🔥 OPTIONAL: Call Ollama (just for logging / future use)
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3", prompt],
                capture_output=True,
                text=True,
                timeout=20
            )
            print("Ollama Output:", result.stdout)
        except Exception as e:
            print("Ollama failed:", e)

        # =========================
        # 🔍 PICK FILE FROM EXISTING OUTPUT
        # =========================
        if not EXISTING_OUTPUT_DIR.exists():
            return {"error": "Output folder not found"}

        files = list(EXISTING_OUTPUT_DIR.glob("*"))

        if not files:
            return {"error": "No files found in output folder"}

        # 👉 Get latest file
        latest_file = max(files, key=os.path.getmtime)

        print("Sending file:", latest_file)

        return FileResponse(
            path=latest_file,
            filename=latest_file.name,
            media_type="application/octet-stream"
        )

    except Exception as e:
        return {"error": str(e)}