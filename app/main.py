from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse, Response
from PIL import Image
import io
import PyPDF2
from .documentai_client import DocumentAIClient

app = FastAPI(title="Document AI Example")

docai = DocumentAIClient()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    # Redirect to the interactive API docs
    return RedirectResponse(url="/docs")


@app.get("/favicon.ico")
async def favicon():
    # Return no content for favicon requests to avoid 404 noise from browsers
    return Response(status_code=204)


@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    # Validate content type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    contents = await file.read()
    try:
        img = Image.open(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to open image: {e}")

    # Example: return size and mode
    return {"filename": file.filename, "content_type": file.content_type, "width": img.width, "height": img.height, "mode": img.mode}


@app.post("/process-pdf")
async def process_pdf(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a PDF")

    contents = await file.read()
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(contents))
        num_pages = len(reader.pages)
        # Extract first page text as example (may be empty)
        first_page = reader.pages[0]
        text = first_page.extract_text() or ""
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read PDF: {e}")

    return {"filename": file.filename, "pages": num_pages, "first_page_text_preview": text[:100]}


@app.post("/documentai/process")
async def documentai_process(file: UploadFile = File(...), project_id: str = "", location: str = "us", processor_id: str = ""):
    """Send uploaded file bytes to Document AI processor. Requires GOOGLE_APPLICATION_CREDENTIALS env var and valid ids.

    Minimal wrapper: returns Document AI response dictionary.
    """
    if not project_id or not processor_id:
        raise HTTPException(status_code=400, detail="project_id and processor_id are required as query params")

    contents = await file.read()
    try:
        res = docai.process_document(project_id, location, processor_id, contents, mime_type=file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document AI processing failed: {e}")

    # Document AI response is a protobuf; convert to dict using its built-in method if available
    try:
        result_dict = {
            "name": getattr(res, "name", None),
            "document_text": getattr(res.document, "text", None) if getattr(res, "document", None) else None,
        }
    except Exception:
        result_dict = {"raw": str(res)}

    return JSONResponse(content=result_dict)
