import os
from typing import Optional


class DocumentAIClient:
    """Lazy wrapper for google-cloud-documentai client.

    Usage: set GOOGLE_APPLICATION_CREDENTIALS env var and pass project/location/processor ids to `process_document`.
    """

    def __init__(self):
        self.client = None

    def _ensure_client(self):
        if self.client is None:
            try:
                from google.cloud import documentai
            except Exception as e:
                raise RuntimeError("google-cloud-documentai is not installed or failed to import") from e

            self.client = documentai.DocumentProcessorServiceClient()

    def process_document(self, project_id: str, location: str, processor_id: str, file_bytes: bytes, mime_type: Optional[str] = None):
        """Send document to Document AI processor and return raw response.

        This is a minimal wrapper. Caller should handle project/location/processor values.
        """
        self._ensure_client()

        name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

        # Construct raw request
        raw_document = {
            "content": file_bytes,
            "mime_type": mime_type or "application/pdf",
        }

        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        return self.client.process_document(request=request)
