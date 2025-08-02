import cv2
import mediapipe as mp
import serial
import time

# Serial configuration
SERIAL_PORT = "COM8"  # Ganti dengan port serial ESP32 Anda (Windows: COM3, Linux/Mac: /dev/ttyUSB0)
BAUD_RATE = 115200

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for ESP32 to initialize
    print(f"Connected to ESP32 on {SERIAL_PORT}")
except Exception as e:
    print(f"Failed to connect to ESP32: {e}")
    exit()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Function to send commands to ESP32 via serial
def send_command(command):
    try:
        ser.write((command + '\n').encode())
        time.sleep(0.1)  # Small delay to ensure command is sent
        
        # Read response from ESP32
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            print(f"Sent: {command}, Response: {response}")
            return response
    except Exception as e:
        print(f"Failed to send command: {command}, Error: {e}")
        return None

# Function to detect the state of each finger
def count_fingers(hand_landmarks):
    # Detect finger states (up or down)
    thumb_up = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x
    index_up = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_up = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_up = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_up = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y
    
    # Combine finger statuses into a list
    finger_status = [thumb_up, index_up, middle_up, ring_up, pinky_up]
    
    # Send control commands to ESP32 for each finger
    send_command("thumb_on" if thumb_up else "thumb_off")
    send_command("index_on" if index_up else "index_off")
    send_command("middle_on" if middle_up else "middle_off")
    send_command("ring_on" if ring_up else "ring_off")
    send_command("pinky_on" if pinky_up else "pinky_off")
    
    # Check if all fingers are down
    if not any(finger_status):
        print("All fingers are down")
        send_command("all_off")
    
    return finger_status

# Initialize VideoCapture
cap = cv2.VideoCapture(0)  # Changed from 1 to 0 (default camera)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

# Variables to control command frequency
last_command_time = 0
command_interval = 0.2  # Send commands every 200ms

print("Starting hand gesture recognition...")
print("Press 'Esc' to exit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect hand landmarks
    results = hands.process(frame_rgb)
    
    current_time = time.time()
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Only send commands at specified intervals to avoid flooding
            if current_time - last_command_time > command_interval:
                fingers = count_fingers(hand_landmarks)
                last_command_time = current_time
    
    # Display status on frame
    cv2.putText(frame, f"Serial Port: {SERIAL_PORT}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, "Press 'Esc' to exit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    cv2.imshow('Hand Gesture Recognition - Serial Control', frame)
    
    if cv2.waitKey(5) & 0xFF == 27:  # Exit on pressing 'Esc'
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
ser.close()
print("Connection closed")
