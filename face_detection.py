# # import os
# # import cv2
# # print("Current working directory:", os.getcwd())

# # # Load the Haar Cascade classifier for face detection
# # face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml') # <-- Update path if needed

# # # Choose a video source: 0 for webcam, or path to a video file
# # video_capture = cv2.VideoCapture(0)  # Use 0 for webcam, change to video file path if needed

# # if not video_capture.isOpened():
# #     print("Error: Could not open video source.")
# #     exit()

# # while True:
# #     # Read frame-by-frame
# #     ret, frame = video_capture.read()

# #     if not ret:
# #         print("Error: Could not read frame.")
# #         break

# #     # Convert the frame to grayscale (Haar Cascades work on grayscale images)
# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# #     # Perform face detection
# #     faces = face_cascade.detectMultiScale(
# #         gray,
# #         scaleFactor=1.1,  # Scale factor for image pyramid
# #         minNeighbors=5,   # Minimum number of neighbors to retain detections
# #         minSize=(30, 30), # Minimum face size
# #         flags=cv2.CASCADE_SCALE_IMAGE
# #     )

# #     # Draw rectangles around the detected faces
# #     for (x, y, w, h) in faces:
# #         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # Green rectangle

# #     # Display the resulting frame
# #     cv2.imshow('Face Detection', frame)

# #     # Exit condition: Press 'q' to quit
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # # When everything is done, release the capture and destroy windows
# # # video_capture.release()
# # video_capture = cv2.VideoCapture('http://192.168.131.46:4747/video', cv2.CAP_FFMPEG)
# # cv2.destroyAllWindows()



# # correct code for droidcam

# import os
# import cv2

# print("Current working directory:", os.getcwd())

# # Load the Haar Cascade classifier for face detection
# face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml') # <-- Update path if needed

# # *** CORRECTED SECTION: Set up video capture for DroidCam URL ***
# droidcam_url = 'http://192.168.131.46:4747/video' # Your DroidCam URL
# video_capture = cv2.VideoCapture(droidcam_url, cv2.CAP_FFMPEG) # Initialize VideoCapture with DroidCam URL and FFMPEG backend

# if not video_capture.isOpened():
#     print(f"Error: Could not open DroidCam stream at: {droidcam_url}") # More informative error message
#     exit()
# # *** END OF CORRECTED SECTION ***

# while True:
#     # Read frame-by-frame
#     ret, frame = video_capture.read()

#     if not ret:
#         print("Error: Could not read frame from DroidCam stream.") # More specific error message
#         break

#     # Convert the frame to grayscale (Haar Cascades work on grayscale images)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Perform face detection
#     faces = face_cascade.detectMultiScale(
#         gray,
#         scaleFactor=1.1,  # Scale factor for image pyramid
#         minNeighbors=5,   # Minimum number of neighbors to retain detections
#         minSize=(30, 30), # Minimum face size
#         flags=cv2.CASCADE_SCALE_IMAGE
#     )

#     # Draw rectangles around the detected faces
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # Green rectangle

#     # Display the resulting frame
#     cv2.imshow('Face Detection', frame)

#     # Exit condition: Press 'q' to quit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything is done, release the capture and destroy windows
# video_capture = cv2.VideoCapture('http://192.168.131.46:4747/video', cv2.CAP_ANY)
# cv2.destroyAllWindows()



"""main code """

import cv2
import face_recognition
import os
import smtplib  # Import smtplib for email
from email.mime.text import MIMEText  # Import MIMEText for email
from email.mime.multipart import MIMEMultipart  # Import MIMEMultipart for email
from email.mime.image import MIMEImage  # Import MIMEImage for image attachments

# *** SECTION: UPDATED EMAIL ALERT FUNCTION (handles image attachments) ***
def send_email_alert(sender_email, sender_password, receiver_email, subject, message, image_data=None):
    """Sends an email alert, optionally with an image attachment."""

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))  # Plain text email body

    if image_data:  # Check if image data is provided
        # Create MIMEImage object using image data
        image = MIMEImage(image_data, name='unknown_face.jpg') # Attachment name is 'unknown_face.jpg'
        msg.attach(image)  # Attach the image to the email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # For Gmail
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email alert sent successfully (with image attachment)!")
    except Exception as e:
        print(f"Error sending email with image: {e}")
# *** END OF SECTION: UPDATED EMAIL ALERT FUNCTION ***

print("Current working directory:", os.getcwd())

# Load the Haar Cascade classifier for face detection (same as before)
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

# *** SECTION 1: Load Known Faces Embeddings and Names (from encode_faces.py - EMBEDDED DIRECTLY HERE for simplicity) ***
known_face_encodings = []  # Initialize empty lists to store known face data
known_face_names = []

known_faces_dir = 'known_faces_images'  # Path to known faces folder (same as in encode_faces.py)

for filename in os.listdir(known_faces_dir):  # Loop through known faces images (same as in encode_faces.py)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        image_path = os.path.join(known_faces_dir, filename)
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

        if face_encodings:  # Only process if face is detected
            face_encoding = face_encodings[0]  # Take the first encoding (assuming one face per image)
            name = os.path.splitext(filename)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)
# *** END OF SECTION 1 ***

if not known_face_encodings:  # Check if any known faces were loaded
    print("Warning: No known faces were encoded. Face recognition will not work.")
else:
    print(f"Loaded {len(known_face_names)} known faces for recognition.")

# Set up video capture (DroidCam URL - or change back to 0 for webcam if needed)
droidcam_url = 'http://10.1.114.250:4747/video'  # Your DroidCam URL
video_capture = cv2.VideoCapture(droidcam_url, cv2.CAP_FFMPEG)

if not video_capture.isOpened():
    print(f"Error: Could not open video source: {droidcam_url}")
    exit()

face_names = []  # List to hold names of recognized faces in the current frame

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Could not read frame from video source.")
        break
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)  # Reduce frame size by half

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB for face_recognition

    face_locations_recognition = face_recognition.face_locations(rgb_frame)  # DETECT FACES AGAIN USING FACE_RECOGNITION (MORE ACCURATE)
    face_encodings_recognition = face_recognition.face_encodings(rgb_frame, face_locations_recognition)  # GENERATE FACE EMBEDDINGS FOR DETECTED FACES

    face_names = []  # Clear face_names list for each frame

    # Loop through each face found in the current frame (using face_recognition's detector)
    for (top, right, bottom, left), face_encoding in zip(face_locations_recognition, face_encodings_recognition):
        name = "Unknown"  # Default name is "Unknown"

        if known_face_encodings:  # Only try to recognize if we have known faces encoded
            # Compare the face encoding in the current frame to the known face encodings
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)  # Adjust tolerance as needed

            if True in matches:  # If there's a match (at least one True in the 'matches' list)
                first_match_index = matches.index(True)  # Find the index of the first match
                name = known_face_names[first_match_index]  # Get the name of the matched known face

        face_names.append(name)  # Add the recognized name (or "Unknown") to the list

        # Draw rectangle and name for each detected face (using face_recognition's locations which are usually more accurate)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Red rectangle for recognition faces (distinguish from Haar)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)  # White text for name

        # *** SECTION: UPDATED EMAIL ALERT TRIGGER CODE (captures face image and sends email with attachment) ***
        if name == "Unknown":
            print("Unknown face detected!")

            # --- Capture and process the unknown face image ---
            unknown_face_image = frame[top:bottom, left:right]  # Extract the face ROI (Region of Interest) from the frame
            if unknown_face_image.size > 0:  # Check if face image is valid
                # Convert face image to JPEG format and get bytes
                is_success, image_buffer = cv2.imencode(".jpg", unknown_face_image)  # Encode to JPEG (you can use .png for PNG)
                if is_success:
                    image_bytes = image_buffer.tobytes()

                    # --- Trigger Email Alert with Image ---
                    sender_email = "nkjsr186582@gmail.com"        # <---- REPLACE THIS WITH YOUR GMAIL ADDRESS
                    sender_password = "urdk ivfz tvdo amrp"  # <---- REPLACE THIS WITH YOUR APP PASSWORD
                    receiver_email = "naveenkumar186582@gmail.com" # <---- REPLACE THIS WITH YOUR RECIPIENT EMAIL ADDRESS
                    alert_subject = "Unknown Face Detected by CCTV System - IMAGE ATTACHED!"  # Subject updated
                    alert_message = "An unknown person has been detected by the CCTV system. An image of the face is attached. Please check the live feed for more details."  # Message updated

                    send_email_alert(sender_email, sender_password, receiver_email, alert_subject, alert_message, image_data=image_bytes)  # Call with image_data
                else:
                    print("Error encoding face image to JPEG for email.")
            else:
                print("Error: Could not extract face image for email.")
        # *** END OF SECTION: UPDATED EMAIL ALERT TRIGGER CODE ***

    cv2.imshow('Face Detection and Recognition', frame)  # Updated window name

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()