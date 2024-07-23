from flask import Flask, request, jsonify, render_template
import openai
import cv2
import os

app = Flask(__name__)

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return jsonify({"response": response['choices'][0]['message']['content'].strip()})

@app.route('/details', methods=['POST'])
def details():
    user_details = request.json
    # Process user details
    return jsonify({"message": "Details received", "details": user_details})

@app.route('/upload_video', methods=['POST'])
def upload_video():
    file = request.files['video']
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Analyze the video
    analysis_result = analyze_video(file_path)

    # Generate response using GPT-4
    prompt = f"The user uploaded a video. Here are the findings: {analysis_result}. Provide feedback and corrective actions."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful injury prevention assistant for athletes."},
            {"role": "user", "content": prompt}
        ]
    )

    # Remove the local file
    os.remove(file_path)

    return jsonify({"response": response['choices'][0]['message']['content'].strip()})

def analyze_video(file_path):
    # Placeholder for video analysis logic
    # Open and process the video using OpenCV
    cap = cv2.VideoCapture(file_path)
    analysis_results = "No significant issues detected."

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Perform analysis on the frame
        # This part would include your model inference code

    cap.release()
    cv2.destroyAllWindows()

    return analysis_results

if __name__ == '__main__':
    app.run(debug=True)
