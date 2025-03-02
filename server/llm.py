import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is not set. Please add it to your .env file.")

client = Groq(api_key=GROQ_API_KEY)

def classify_doordash_order(ocr_text: str) -> bool:
    """
    Uses Groq's Llama model to classify if the user is on the DoorDash website.
    Returns True (YES) if it is a DoorDash-related page, False (NO) otherwise.
    """
    prompt = f"""
    You are an AI classifier. Your task is to analyze the given OCR text and determine if the user 
    is currently on the **DoorDash website or app**.

    **DOORDASH PAGE DETECTION CRITERIA:**
    - Presence of the "DoorDash" logo or website header.
    - Navigation menu items like "Home," "Grocery," "Retail," "Orders," "Account."
    - Restaurant listings with names, ratings (e.g., 4.5★), delivery times, and fees.
    - Keywords like "Start free trial," "Delivery Fee," "DashPass," "Order Now."
    - Checkout-related elements: "Cart," "Place Order," "Your total is $XX.XX."

    **INSTRUCTIONS:**
    - If the OCR text contains multiple indicators that strongly suggest the user is on the DoorDash website, 
      return **exactly "YES"**.
    - If the text is unrelated to DoorDash, return **exactly "NO"**.

    **Examples:**
    - OCR Text: "DOORDASH Home Grocery Retail Convenience Beauty Pets Health Orders Account"
      **Output: YES**

    - OCR Text: "Your DoorDash order total is $19.99. Click 'Place Order' to confirm."
      **Output: YES**

    - OCR Text: "Tracking your food delivery with DoorDash."
      **Output: YES**

    - OCR Text: "McDonald's, 4.5★, $0.99 delivery fee, 20 min"
      **Output: YES**

    - OCR Text: "UberEats, Postmates, GrubHub, order now."
      **Output: NO**

    - OCR Text: "{ocr_text}"
      **Output:**
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2,
        )

        answer = response.choices[0].message.content.strip().upper()
        return answer == "YES"

    except Exception as e:
        print(f"❌ Error classifying DoorDash page: {e}")
        return False
