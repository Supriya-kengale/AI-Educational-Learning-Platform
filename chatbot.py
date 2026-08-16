import requests
import os
import json
from flask import jsonify

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCdn9YZl1TJqvrtqzG5j1RMepVk-fMtlDU")
# Using the most basic and widely available model
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

def get_chat_response(user_message: str):
    if not user_message.strip():
        # Return a dictionary instead of using jsonify directly
        return {"reply": "Please ask me something 🙂"}

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{
                "text": f"You are a helpful AI tutor for Smart3D Learning. Please provide educational assistance related to the subjects taught in this platform (Biology, Computer Science, Mathematics, Physics, Chemistry, and AI). Keep your responses concise, informative, and educational. User question: {user_message}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1000
        }
    }

    try:
        print(f"Sending request to Gemini API with message: {user_message}")
        response = requests.post(GEMINI_URL, headers=headers, json=data)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error response content: {response.text}")
            # Return a dictionary instead of using jsonify directly
            return {"reply": f"API Error: {response.status_code} - {response.text}"}
            
        response.raise_for_status()
        result = response.json()
        print(f"Response received successfully")
        
        # Extract the response text from Gemini's response format
        if "candidates" in result and len(result["candidates"]) > 0 and "content" in result["candidates"][0]:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            # Return a dictionary instead of using jsonify directly
            return {"reply": reply}
        else:
            # Return a dictionary instead of using jsonify directly
            return {"reply": "I couldn't generate a response. Please try rephrasing your question."}
    except Exception as e:
        print("Gemini API Error:", e)
        # Return a dictionary instead of using jsonify directly
        return {"reply": f"Sorry, I am facing issues right now. Error: {str(e)}"}