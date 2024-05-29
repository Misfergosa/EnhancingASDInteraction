#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import string
import openai
import os
import random
from gtts import gTTS
import speech_recognition as sr
from IPython.display import HTML, display
from base64 import b64encode
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import pygame


def process_camera_with_emotion_detection(camera_index=0):
  # Load YOLO model
  model = YOLO(r"emotion.pt")
  names = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprised']

  # Open video capture
  cap = cv2.VideoCapture(camera_index)
  assert cap.isOpened(), "Error opening camera."

  # Get frame dimensions and FPS
  w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

  last_detection_time = cv2.getTickCount()  # Initialize detection timer

  while cap.isOpened():
    success, frame = cap.read()
    if not success:
      print("Video frame is empty or processing complete.")
      break

    # Check if 5 seconds have passed since the last detection
    if (cv2.getTickCount() - last_detection_time) / cv2.getTickFrequency() >= 1:
      results = model.predict(frame, show=False)

      if results is not None:  # Check if predictions exist
        boxes = results[0].boxes.xyxy.cpu().tolist()
        clss = results[0].boxes.cls.cpu().tolist()

        if boxes:  
          detected_emotion = names[int(clss[0])]
          return detected_emotion
      last_detection_time = cv2.getTickCount()
    cv2.imshow("Emotion Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
      break

  cap.release()
  cv2.destroyAllWindows()

# -----------------------  Camera process_camera_with_game_detection ----------------------- #


def process_camera_with_game_detection(camera_index=0):

  # Load YOLO model
  model = YOLO(r"RPS.pt")
  names = ['paper', 'rock', 'scissors']

  # Open video capture
  cap = cv2.VideoCapture(camera_index)
  assert cap.isOpened(), "Error opening camera."

  # Get frame dimensions and FPS
  w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

  last_detection_time = cv2.getTickCount()  # Initialize detection timer

  while cap.isOpened():
    success, frame = cap.read()
    if not success:
      print("Video frame is empty or processing complete.")
      break

    # Check if 5 seconds have passed since the last detection
    if (cv2.getTickCount() - last_detection_time) / cv2.getTickFrequency() >= 1:
      results = model.predict(frame, show=False)

      if results is not None:  # Check if predictions exist
        boxes = results[0].boxes.xyxy.cpu().tolist()
        clss = results[0].boxes.cls.cpu().tolist()

        if boxes: 
          detected_game = names[int(clss[0])]
          return detected_game 

      last_detection_time = cv2.getTickCount() 

    cv2.imshow("User Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
      break

  cap.release()
  cv2.destroyAllWindows()






# End of detiction 




# Set up OpenAI API key
openai.api_key = "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"

# Define the choices for the game
choices = ["rock", "paper", "scissors"]

# Function to play Rock, Paper, Scissors game
def play_game(user_choice, assistant_choice):
    #assistant_choice = random.choice(choices)
    if user_choice == assistant_choice:
        return "تعادلنا"
    elif (user_choice == "rock" and assistant_choice == "scissors") or \
         (user_choice == "paper" and assistant_choice == "rock") or \
         (user_choice == "scissors" and assistant_choice == "paper"):
        return "مبروك انت ذكي!"
    elif (assistant_choice == "rock" and user_choice == "scissors") or \
         (assistant_choice == "paper" and user_choice == "rock") or \
         (assistant_choice == "scissors" and user_choice == "paper") :
        return "انا ربحت لنحاول مره اخرى"

def get_completion(prompt, conversation_history, model="gpt-3.5-turbo"):
    conversation_history.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages=conversation_history,
        temperature=0
    )
    response_message = response.choices[0].message["content"]
    conversation_history.append({"role": "assistant", "content": response_message})
    return response_message

def recognize_speech(language="ar-SA", device_index=0):
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=device_index)
    mic_list = sr.Microphone.list_microphone_names()
    print("Available microphones:", mic_list)

    with mic as source:
        #emotionResult = process_camera_with_emotion_detection()
        print("Say something!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=language)
        print("You said:", text)
        #process_camera_with_emotion_detection()
        #process_camera_with_game_detection()
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""
        
def generate_audio(text, language="ar"):
  # Generate a random filename with letters and numbers
    filename = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10)) + ".mp3"
  
  # Create the audio object with gTTS
    output = gTTS(text=text, lang=language, slow=False)
  
  # Save the audio with the random filename
    output.save(filename)
  
  # Return the filename
    return filename

def display_audio(audio_path):
    try:
        # Initialize pygame
        pygame.init()
        
        # Load the audio file
        pygame.mixer.music.load(audio_path)
        
        # Play the audio file
        pygame.mixer.music.play()
        
        # Wait until the audio finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Remove the temporary audio file if it exists
        #if os.path.exists(audio_path):
         #   os.remove(audio_path)
            print('Done')

# Example usage:
#display_audio("response.mp3")


def chat_loop():
    print("Welcome to the GPT Chat! Type 'exit' to quit or speak to start.")
    conversation_history = []
    system_message = {"role": "system", "content": "ِAlways Speck in Arabic. You are communicating with a 10-year-old child. Use simple, concrete language, short sentences, and visual examples where possible. Be patient, understanding, and encouraging.Do not mention if he is 10-year-old child and ASD. Focus on their interests and communication style to make the conversation enjoyable and engaging. Ask if he want to start a story or play a game. Stroy 'rabbit and turtle' should in berif. When you finish story ask if he want to play a game Rock scissors paper. Ask him if he want to see me Dance"}
    conversation_history.append(system_message)
    
    while True:
        user_input = recognize_speech()
        if user_input.lower() == "exit":
            break

        if user_input:  # Check if speech was recognized
            if "اريد اللعب" in user_input.lower():
                user_choice = process_camera_with_game_detection()
                # Robot should do something 
                assistant_choice = random.choice(choices)
                response = play_game(user_choice, assistant_choice)
                pub.publish('واحد')
                pub.publish('اثنان')
                pub.publish('ثلاثة')
                pub.publish(assistant_choice)
                
                if "مبروك انت ذكي" in response.lower():
                   print('ok')
                   pub.publish('تصفيق')
                   pub.publish('رقص')
                
                
                print(user_choice, assistant_choice)
            else:
                response = get_completion(user_input, conversation_history)
                print("GPT:" , response)
                if "نرقص " in response.lower():
                   pub.publish('رقص')
                elif "وعليكم السلام" in response.lower():
                   pub.publish('سلام')
                   
            audio_file_path = generate_audio(response, language='ar')  # Generate audio in Arabic
            display_audio(audio_file_path)  # Play the generated audio
        else:
            print("Sorry, I couldn't understand. Please try again.")

if __name__ == "__main__":
    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('Word', String, queue_size=10)
    
    chat_loop()

