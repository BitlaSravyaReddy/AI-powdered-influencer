# #from langchain_google_genai import ChatGoogleGenerativeAI
# from pathlib import Path
# import asyncio

# from browser_use import Agent, BrowserSession
# from browser_use.llm import ChatGoogle


# llm = ChatGoogle(model="gemini-2.0-flash", api_key="AIzaSyB3bTFSbph48oMQXTohSI9VnzkCrL8LUVc")


# browser=BrowserSession(
#     headless=True,
# 	keep_alive=True,
# 	executable_path=Path('C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe')  # ✅ wrap in Path

# )
# navbar_str = ['How it works' ,'Usecases','Features', 'Pricing']


# async def main():
#     await browser.start()
#     agent= Agent(
#         task="Go to 'https://neura-app.com/' and inspect only the header or navbar section of the page.",
#         llm=llm,
#         browser_session=browser
#     )

#     await agent.run()

#     async def get_review(element: str):
#         agent1 = Agent(
#             task=f"Explore the navbar element {element} and provide a review.",
#             llm=llm,
#             browser_session=browser,
            
#         )
#         history = await agent1.run()
#         return history.final_result() 
#     for element in navbar_str:
#         review = await get_review(element)
#         print(f"{element}: {review}")

#     await browser.kill()    
# if __name__ == "__main__":
#     asyncio.run(main())
from browser_use import Agent, BrowserSession
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
from dotenv import load_dotenv
import os
import pyttsx3


load_dotenv()  

tts = pyttsx3.init()
tts.setProperty('rate', 150)
def speak(text):
        """Speak text using TTS"""
        print(f"🎤 Speaking: {text}")
        tts.say(text)
        tts.runAndWait()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key="AIzaSyB3bTFSbph48oMQXTohSI9VnzkCrL8LUVc")
navbar_str = ['How it works', 'Usecases', 'Features', 'Pricing']
async def main():
    browser_session = BrowserSession(keep_alive=True , headless=True,
                                     executable_path="C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")  
    await browser_session.start()
    
    # First agent to inspect the navbar
    agent = Agent(
        task="Go to 'https://neura-app.com/'",
        llm=llm,
        browser_session=browser_session
    )
    await agent.run()

    async def get_review(element: str):
        # Create a new agent for each element review
        agent_review = Agent(
            task=f"Click on the navbar element: {element} and provide a review on it in 2-3 sentences.",
            llm=llm,
            browser_session=browser_session,  # Reuse the same browser session
        )
        history = await agent_review.run()
        return history.final_result() 
    
    for element in navbar_str:
        review = await get_review(element)
        print(f"{element}: {review}")
        speak(f"{element}: {review}")

    await browser_session.close()  # Properly close the browser session

if __name__ == "__main__":
    asyncio.run(main())