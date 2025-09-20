# FastAPI Document AI Example

A small FastAPI app that demonstrates:
- Image processing with Pillow
- PDF handling with PyPDF2
- A placeholder integration with Google Cloud Document AI

Requirements
- Python 3.9+

Setup (PowerShell on Windows)

```powershell
# Create and activate a venv (PowerShell). If activation is blocked by execution policy, the second line shows a temporary workaround.
python -m venv .venv
# Normal activation (dot-sourcing) - run from PowerShell prompt:
. .\.venv\Scripts\Activate.ps1
# If activation is blocked, run this to allow scripts for the current process only, then activate:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run

```powershell
uvicorn app.main:app --reload --port 8000
```

Notes
- Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to your service account JSON to use Document AI.
- The Document AI endpoint in this repo is a placeholder showing how to wire the client. You may need to adapt project/location/processor IDs.

Troubleshooting: "error: subprocess-exited-with-error" during pip install
 - This frequently happens when pip attempts to build a package from source (commonly Pillow) and required build tools or compatible binary wheels are not available for your Python version.
 - Remedies:
	 - Use a supported Python version with prebuilt wheels (Python 3.11 is recommended on Windows).
	 - Loosened the Pillow pin in `requirements.txt` so pip can select a compatible binary wheel if available.
	 - If you must build from source, install the necessary build tools:
		 - Install the "Build Tools for Visual Studio" with C++ build tools.
		 - Ensure you have a recent version of setuptools and wheel: `python -m pip install --upgrade pip setuptools wheel`.
	 - If you still see the error, paste the pip output here and I can help diagnose the missing build dependency.
