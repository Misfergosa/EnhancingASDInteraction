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
import time


def process_camera_with_emotion_detection(camera_index=0):
  # Load YOLO model
  model = YOLO(r"HappySadNeutral (2).pt")
  names = [ 'happy', 'neutral', 'sad']

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




choices = [ "paper", "scissors"]
def play_game(user_choice, assistant_choice):
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

def game_statue(greeting_text):
    greeting_text = greeting_text
    greeting_audio_path = generate_audio(greeting_text, language='ar')
    display_audio(greeting_audio_path)
    
# Function to play Rock, Paper, Scissors game 
# Set up OpenAI API key
openai.api_key = "sk-proj-4bCupZuHh43H0eiRkmlIT3BlbkFJqQpIXm3EZBknGhD1IvcR"
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
    
    with mic as source:
        print("Say something!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        text = recognizer.recognize_google(audio, language=language)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio. Please type your input:")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""    


def generate_audio(text, language="ar"):
    filename = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10)) + ".mp3"
    output = gTTS(text=text, lang=language, slow=False)
    output.save(filename)
    return filename

def display_audio(audio_path):
    try:
        pygame.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
            print(' ')


def emotion_user():
    process_camera_with_emotion_detection()


            
def greet_user():
    greeting_text = "السلام عليكم صديقي العزيز"
    greeting_audio_path = generate_audio(greeting_text, language='ar')
    display_audio(greeting_audio_path)

  
def greet_user1():
    greeting_text1 ="هل تريد اللعب، سماع قصة، أو الرقص؟"
    greeting_audio_path1 = generate_audio(greeting_text1, language='ar')
    display_audio(greeting_audio_path1)
      
    
def chat_loop():
    print("Welcome to the GPT Chat! Type 'exit' to quit or speak to start.")
    conversation_history = []
    prompot = "Your name is Twaiq and your age is 10 year old. ِAlways Speack in Arabic. You are communicating with a 10-year-old child. Use simple, concrete language, short sentences, and visual examples where possible. Be patient, understanding, and encouraging.Do not mention if he is 10-year-old child and ASD. Focus on their interests and communication style to make the conversation enjoyable and engaging.You ask how you can help and classify the response to one of these classes ['Dance', 'Play', 'Visual QA', 'Chat', 'Story', 'End conversation', 'None'] give me the output in this way: class and this should be one of the above classes and then your response."
    system_message = {"role": "system", "content": prompot}
    conversation_history.append(system_message)
    score = {"user": 0, "assistant": 0}    
    while True:
        user_input = recognize_speech().lower()

        if user_input:  # Check if speech was recognized
            response = get_completion(user_input, conversation_history)
            print("GPT:", response)
            response = response.replace("response: ", "")
            # Classify response
            if 'End conversation' in response:
            	print("Class: End conversation", response)
            	break

            elif "dance" in response.lower():
                print("Class: Dance", response)
                pub.publish('رقص')
                pub.publish('رقص')               
            elif "play" in response.lower():
            	
                response = response.replace("class: Play", "")
                game_statue("هيا لنلعب حجره! , ورقة! , مقص!")
                while True:
                    user_choice = process_camera_with_game_detection()
                    assistant_choice = random.choice(choices)
                    pub.publish(assistant_choice)
                    result = play_game(user_choice, assistant_choice)
                    
                    if "تعادلنا" == result:
                     
                        print("It's a tie! Let's try again.")
                        
                    elif "مبروك انت ذكي!" == result:
                        pub.publish('تصفيق')
                        print("Congratulations, you're smart. You won!")
                       
                        score["user"] += 1
                    elif "انا ربحت لنحاول مره اخرى" == result:
                        print("I won!")
                        
                        score["assistant"] += 1
                    
                    time.sleep(5)   
                    game_statue(result)
                    #game_statue("النتيجة كتالي!")    
                    game_statue(f"أنت - {score['user']}, انا - {score['assistant']}")
                    #game_statue(" هل تريد اللعب مره اخرى ")
                    #game_statue("  نعم! ام لا!")
                    play_again = recognize_speech()
                    if "لا" in play_again:
                        break
            elif "chat" in response.lower():
                response = response.replace("Response:", "")
                response = response.replace("class: Chat", "")
                print("Class: Chat", response)
            elif "story" in response.lower():
                
                response = response.replace("class: Story", "")
                print("Class: Story", response)
                #pub.publish('تصفيق')
                game_statue("قصة الأرنب والسلحفاة كانَ يَحْكى أنَّهُ كانَ ثَمَّ أرنبٌ سريعٌ جدًّا يَتَباهى بِسُرعَتِهِ ويَتحدَّى كُلَّ مَنْ يُقابِلُهُ في سَباقٍ. في يومٍ مِنَ الأيَّامِ، تحدَّى الأرنبُ سَلَحْفَاةً بطيئةً، مُعتقدًا أنَّهُ سَيَفُوزُ بِسهولةٍ. انطلقَ الأرنبُ سريعًا جدًّا، تارِكًا السَّلحْفَاةَ بعيدًا وراءَهُ. ثُمَّ شَعَرَ الأرنبُ بِالثِّقَةِ الزَّائدةِ، فَقرَّرَ أنْ يَأْخُذَ قَسْطًا مِنَ الرَّاحةِ على الطَّريقِ. بينما كانَ الأرنبُ يَنَامُ، واصلتْ السَّلحْفَاةُ التَّقَدُّمَ بِثباتٍ. عندما استيقظَ الأرنبُ، اكتشفَ أنَّ السَّلحْفَاةَ قدْ وَصَلَتْ إلى خَطِّ النِّهَايةِ وفازَتْ بِالسَّباقِ. تَعَلَّمَ الأرنبُ مِنْ هَذِهِ القصةِ أنَّ المُثابرةَ والتصميمَ يَنْتَصِرَانِ على الغُرورِ والتَّسرُّعِ. ")
                game_statue("ِشكراً لحسن أستماعك")
                pub.publish('تصفيق')
            elif "visual qa" in response.lower():
                print("Class: Visual QA", response)
            else:
                print("Class: None", response)

         
             
            audio_file_path = generate_audio(response, language='ar')
            display_audio(audio_file_path)

        else:
            print("Sorry, I couldn't understand. Please try again.")
            #break

          

if __name__ == "__main__":
    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('Word', String, queue_size=10)
    time.sleep(1)
    while True:
        pub.publish('سلام')
        greet_user()
        
        emotion = emotion_user()
        greet_user1()
        
        chat_loop()
    
    
