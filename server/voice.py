import os
import requests
from dotenv import load_dotenv

load_dotenv()

VAPI_AUTH_TOKEN   = os.getenv("VAPI_AUTH_TOKEN")
PHONE_NUMBER_ID   = os.getenv("VAPI_PHONE_NUMBER_ID")
TEST_NUMBER       = os.getenv("TEST_NUMBER")
VAPI_ENDPOINT     = os.getenv("VAPI_ENDPOINT", "https://api.vapi.ai/call")

def call_with_future_amit():
    if not all([VAPI_AUTH_TOKEN, PHONE_NUMBER_ID, TEST_NUMBER]):
        print("❌ Missing environment variables. Please check .env.")
        return

    headers = {
        "Authorization": f"Bearer {VAPI_AUTH_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "type": "outboundPhoneCall",
        "phoneNumberId": PHONE_NUMBER_ID,
        "customer": {
            "number": TEST_NUMBER,
        },
        "name": "Future Amit",

        "assistant": {
            "firstMessage": (
                "Hey, it's Future Amit again! Ready to roast your DoorDash habit. "
                "Let's talk about that money you're about to blow!"
            ),
            "model": {
                "provider": "groq",
                "model": "llama-3.3-70b-versatile",  
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are 'Future Amit' calling from the future, with comedic flair. "
                            "Your mission is to *roast* the user lightly about their DoorDash addiction, "
                            "use humor and a dash of sarcasm to make them feel a little guilty, yet amused. "
                            "Highlight how they've wasted money in the past. Then shift to encouraging them "
                            "to cook something simple (like leftover groceries or quick pasta) instead of ordering. "
                            "If they absolutely insist on ordering, remind them of how broke they felt last week. "
                            "Speak slowly, with comedic confidence, and end the call if they agree to cook or they request to stop. "
                            "Feel free to mention 'budget meltdown' or 'future regret' in a playful tone."
                        ),
                    },
                ],
                "toolIds": []
            },
            "voice": {
                "provider": "cartesia",
                "voiceId": "638efaaa-4d0c-442e-b701-3fae16aad012"
            },
            "stopSpeakingPlan": {
                "numWords": 0,
                "voiceSeconds": 0.2,
                "backoffSeconds": 1,
                "acknowledgementPhrases": [
                    "okay", "fine", "I'll cook", "you're right", "stop", "bye", "cancel the call"
                ],
                "interruptionPhrases": [
                    "stop", "shut", "enough", "quiet", "cancel", "wait", "nope", "nah", "nevermind"
                ]
            },
            "endCallPhrases": [
                "I'll cook", "You're right", "Not ordering", "Cancel", "Hanging up", "Bye", "End call"
            ],
            "endCallMessage": (
                "Alright, I've done my job. Future You is proud. Bon appétit—just not from DoorDash!"
            )
        }
    }

    resp = requests.post(VAPI_ENDPOINT, headers=headers, json=payload)

    if resp.status_code in (200, 201):
        print("📞 Call created successfully!")
        print("Response:", resp.json())
    else:
        print(f"❌ Error creating call: HTTP {resp.status_code}")
        print("Response:", resp.text)


if __name__ == "__main__":
    call_with_future_amit()
