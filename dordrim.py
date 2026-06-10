import cv2

droidcam_url = ' *** ' # Your DroidCam URL

cap = cv2.VideoCapture(droidcam_url)

if not cap.isOpened():
    print("Error: Could not open DroidCam stream.")
    exit()

ret, frame = cap.read()

if not ret:
    print("Error: Could not read frame from DroidCam stream.")
    cap.release()
    exit()

cv2.imshow('DroidCam Test Frame', frame)
cv2.waitKey(0) # Wait for a key press to close the window

cap.release()
cv2.destroyAllWindows()


sender_email = "***"        # <---- REPLACE THIS WITH YOUR GMAIL ADDRESS
sender_password = "***"  # <---- REPLACE THIS WITH YOUR APP PASSWORD
receiver_email = "***"    # <---- REPLACE THIS WITH THE GMAIL ON WHICH YOU WANT TO RECEIVE THE MAIL
