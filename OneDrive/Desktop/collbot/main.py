import openai
import os
from flask import Flask, request, jsonify

# Set your OpenAI API key

openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_role = data.get("role")
    query = data.get("query")
    
    # Generate the response based on user role and query
    response = get_chatbot_response(user_role, query)
    
    # Return the response to the frontend
    return jsonify({"response": response})

def get_chatbot_response(user_role, query):
    if user_role == "student":
        prompt = f"Student Query: {query}. Provide an informative response related to student tasks like fee payment, course registration, or exam schedules."
    elif user_role == "teacher":
        prompt = f"Teacher Query: {query}. Provide an answer related to teaching tasks like course updates or student progress."
    elif user_role == "parent":
        prompt = f"Parent Query: {query}. Provide a helpful response regarding their child's progress, fees, or academic events."
    elif user_role == "outsider":
        prompt = f"Outsider Query: {query}. Provide general information about the college, admission, courses, and events."

    # Make the API call to OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other models like GPT-4 if you have access
        prompt=prompt,
        max_tokens=150  # Adjust the length of the response
    )

    # Extract the generated response from OpenAI
    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(debug=True)
