import face_recognition
import cv2
import numpy as np
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
image_of_mark =	face_recognition.load_image_file('./mark.jpg')
mark_face_encoding = face_recognition.face_encodings(image_of_mark)[0]
image_of_gates = face_recognition.load_image_file('./old_gates.jpg')
gates_face_encoding = face_recognition.face_encodings(image_of_gates)[0]
image_of_me = face_recognition.load_image_file('./me.jpg')
me_face_encoding = face_recognition.face_encodings(image_of_me)[0]

# Create arrays of encodings and names
known_face_encodings = [ mark_face_encoding, gates_face_encoding, image_of_me]
known_face_names = ["mark", "gates", "danbi"]

# known_face_encodings =	[ mark_face_encoding, gates_face_encoding]
# known_face_names =	["mark", "gates"]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size top*=4
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        # Display the resulting image
        cv2.imshow('Video', frame)
        
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()