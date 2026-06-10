import face_recognition
import os
import cv2  # Import OpenCV for image loading if needed

# Path to the folder containing known faces images
known_faces_dir = 'known_faces_images'  # <-- Make sure this is correct! (Should be 'known_faces_images' if folder is in same directory as script)

known_face_encodings = []
known_face_names = []

# Loop through each image file in the folder
for filename in os.listdir(known_faces_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')): # Process image files only
        image_path = os.path.join(known_faces_dir, filename)
        print(f"Processing image: {image_path}")

        # Load image using face_recognition (or OpenCV if you prefer)
        # image = face_recognition.load_image_file(image_path) # Using face_recognition's loader
        image = cv2.imread(image_path) # Using OpenCV's image loader (can be more robust sometimes)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Convert BGR to RGB for face_recognition

        # Detect faces in the image
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

        if not face_encodings:
            print(f"Warning: No faces found in {filename}. Skipping.")
            continue

        # Assuming each image is of one known person, use the filename (without extension) as the name
        name = os.path.splitext(filename)[0] # Use filename without extension as name

        # Add face encodings and name to lists
        for face_encoding in face_encodings:
            known_face_encodings.append(face_encoding)
            known_face_names.append(name) # Or you could use a more descriptive name if needed

print("Known faces encoded and database created.")

# You can optionally save the encodings and names to a file (e.g., using pickle or JSON) for later use
# For now, we'll keep them in memory.