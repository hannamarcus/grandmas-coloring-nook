from flask import Flask, request, send_file, render_template
import cv2
import os

# Flask app setup
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Pencil sketch transformation function
def create_pencil_sketch(input_path, output_path):
    """
    Converts an input image into a pencil sketch effect.
    """
    # Read the original image
    image = cv2.imread(input_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    inverted_gray = cv2.bitwise_not(gray)

    # Apply Gaussian blur to the inverted image
    blurred = cv2.GaussianBlur(inverted_gray, (21, 21), 0)

    # Create the pencil sketch effect using color dodge
    sketch = cv2.divide(gray, 255 - blurred, scale=256)

    # Save the resulting pencil sketch image
    cv2.imwrite(output_path, sketch)

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle the uploaded file
        file = request.files["file"]
        if file:
            # Save the uploaded file to the uploads folder
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            # Set the output path for the sketch
            output_path = os.path.join(OUTPUT_FOLDER, f"coloring_nook_{file.filename}")

            # Process the image to create a pencil sketch
            create_pencil_sketch(input_path, output_path)

            # Send the output file back to the user
            return send_file(output_path, mimetype="image/jpeg")

    # Render the HTML upload form
    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
