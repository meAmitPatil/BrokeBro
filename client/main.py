import requests
import time
import json

SP_URL = "http://localhost:3030"
BACKEND_URL = "http://localhost:8000"
INTERVAL = 20
MAX_RETRIES = 3

def get_screenpipe_activity():
    """Get latest OCR info from ScreenPipe"""
    print("🔍 Fetching latest OCR data from ScreenPipe...")
    retries = 0

    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{SP_URL}/search?limit=1&offset=0&content_type=ocr", timeout=(10, 20)
            )
            response.raise_for_status()
            print("✅ OCR data fetched successfully!")
            data = response.json()

            if not data.get("data"):
                print("⚠️ No OCR data found. Skipping this cycle.")
                return None
            
            return data

        except requests.exceptions.Timeout:
            print(f"⚠️ Request timed out. Retrying ({retries+1}/{MAX_RETRIES})...")
            retries += 1
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching ScreenPipe data: {e}")
            return None
    
    print("❌ Max retries reached. Skipping this cycle.")
    return None

def main():
    """Run OCR processing on an interval"""
    while True:
        ocr_data = get_screenpipe_activity()
        if not ocr_data:
            print(f"⏳ Snoozing for {INTERVAL} seconds before next check...")
            time.sleep(INTERVAL)
            continue

        print(f"📤 Posting OCR data to backend: {ocr_data}")
        try:
            response = requests.post(f"{BACKEND_URL}/handle_ocr", json=ocr_data, timeout=(10, 20))
            response.raise_for_status()
            print(f"✅ Request posted successfully! Server Response: {response.status_code}")
        except requests.exceptions.Timeout:
            print("⚠️ Backend request timed out. Skipping this cycle.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error posting to backend: {e}")

        print(f"⏳ Snoozing for {INTERVAL} seconds before next check...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
