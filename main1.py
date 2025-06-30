
import asyncio
import subprocess
import time
import pyttsx3
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserSession, Controller
from pathlib import Path
from pydantic import BaseModel
from typing import List


class Post(BaseModel):
	post_title: str
	post_url: str

class Posts(BaseModel):
	posts: List[Post]
	
controller = Controller(output_model=Posts) 
class RealTimeInfluencer:
    def __init__(self):
        # Setup TTS engine
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)
        
        # Setup LLM
# AIzaSyB3bTFSbph48oMQXTohSI9VnzkCrL8LUVc
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite-001")
        self.recording_process = None
        
    def start_recording_with_mic(self):
        """Start screen + microphone recording using FFmpeg"""
        output_file = f"influencer_video_{int(time.time())}.mp4"
        
        # FFmpeg command to record screen + microphone
        cmd = [
            'ffmpeg',
            '-f', 'gdigrab', '-i', 'desktop',  # Screen capture (Windows)
            '-f', 'dshow', '-i', 'audio=Microphone Array (Realtek(R) Audio)',  # Mic audio (Windows)
            '-c:v', 'libx264', '-preset', 'ultrafast',
            '-c:a', 'aac',
            '-movflags', '+faststart',
            '-y', output_file
        ]
        
        self.recording_process = subprocess.Popen(cmd)
        print(f"Recording started: {output_file}")
        return output_file
    
    def speak(self, text):
        """Speak text using TTS"""
        print(f"🎤 Speaking: {text}")
        self.tts.say(text)
        self.tts.runAndWait()
    
    async def run_with_narration(self):
        

        # Start recording
        output_file = self.start_recording_with_mic()
        
        try:
            # Introduction
            browser_session = BrowserSession(
    headless=False,
    keep_alive=True,
    wait_for_network_idle_page_load_time=3.0,
    allowed_domains=['*.producthunt.com', '*'],
    executable_path=Path('C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe')  # ✅ wrap in Path
)

            await browser_session.start() 

            agent1 = Agent(
                task="Navigate to https://producthunt.com and explore the homepage",
                llm=self.llm,
                browser_session=browser_session
            )
            await agent1.run()
            self.speak("Hey everyone! Welcome back to my channel. Today I'm exploring the hottest AI tools on Product Hunt!")
            
            # Task 1: Navigate
            self.speak("Let's head over to Product Hunt and see what's trending")
            
            
            # Task 2: Search
            self.speak("Now I'm going to search for AI tools to find the most innovative products")
            agent2 = Agent(
                task="Search for top two products on Product Hunt and browse the results and get their  names",
                llm=self.llm,
                browser_session=browser_session,
                controller=controller
            )
            history = await agent2.run()
            res = history.final_result()
            print(res)
            if res:
                parsed: Posts = Posts.model_validate_json(res)
                if parsed.posts:
                        first_post = parsed.posts[0]
                        first_product_name= first_post.post_title
                        first_product_url=first_post.post_url
                        second_post = parsed.posts[1]
                        second_product_name = second_post.post_title
                        second_product_url= second_post.post_url
            self.speak(f"We have {first_product_name} and {second_product_name} as our Top products of the day")            
                        
            print(".")
            print(".")
            self.speak("Let me click on these fascinating AI products to see what they offer")
            agent3 = Agent(
                task=f"Click on the top {first_product_name} and visit its site using 'visit website' option on the page itself",
                llm=self.llm,
                browser_session=browser_session
            )
            await agent3.run()
            agent4 = Agent(
            task="Give review of the website Ui (how it looks like )",
                llm=self.llm,
                browser_session=browser_session
            )
            history= await agent4.run()
            self.speak(history.final_result)
            


            self.speak("I'm checking out the user reviews and ratings to see what the community thinks")
            agent5 = Agent(
                task="Look at ratings and user comments for the AI tools",
                llm=self.llm,
                browser_session=browser_session
            )
            await agent5.run()
            
            # Conclusion
            self.speak("That's a wrap! These AI tools look incredible. Let me know in the comments which one you're most excited about!")
            browser_session = BrowserSession(keep_alive=False)

            await browser_session.close()
        finally:
            # Stop recording
            if self.recording_process:
                self.recording_process.terminate()
                print(f"Recording saved: {output_file}")
        
        return output_file

async def main():
    
    influencer = RealTimeInfluencer()
    video_file = await influencer.run_with_narration()
    print(f"Video recorded and saved as: {video_file}")

if __name__ == "__main__":
    asyncio.run(main())
