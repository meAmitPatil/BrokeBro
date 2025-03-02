from fastapi import FastAPI, Request, HTTPException
from typing import Dict, Any
import logging

from llm import classify_doordash_order
from voice import call_with_future_amit

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/handle_ocr")
async def handle_ocr(request: Request) -> Dict[str, Any]:
    try:
        data = await request.json()

        if "data" not in data or not isinstance(data["data"], list) or not data["data"]:
            raise HTTPException(status_code=400, detail="Invalid OCR data format: Missing 'data' field.")

        ocr_text = data["data"][0]["content"].get("text", "").strip()
        if not ocr_text:
            raise HTTPException(status_code=400, detail="No text found in OCR data.")

        doordash_detected = classify_doordash_order(ocr_text)
        logger.info(f"🤖 DoorDash Order Detected: {doordash_detected}")

        if doordash_detected:
            logger.info("🚀 Triggering Future Amit call to prevent impulsive purchase!")
            call_with_future_amit()

            return {
                "status": "triggered",
                "message": "DoorDash event detected. Future Amit is calling you!"
            }

        return {
            "status": "ignored",
            "message": "Not a DoorDash event."
        }

    except Exception as e:
        logger.error(f"❌ Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
