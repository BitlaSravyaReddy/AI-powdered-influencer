from browser_use import Agent, BrowserSession, Controller
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import List
import pyttsx3
load_dotenv()

# for text-to-speech(TTS)
tts = pyttsx3.init()
tts.setProperty('rate', 150)
def speak(text):
    """Speak text using TTS"""
    print(f"🎤 Speaking: {text}")
    tts.say(text)
    tts.runAndWait()

# Data models for posts used to structure the output of the llm
class Post(BaseModel):
	post_title: str
	post_url: str

class Posts(BaseModel):
	posts: List[Post]    

controller1=Controller(output_model=Posts)	
	

llm= ChatGoogleGenerativeAI(model="gemini-2.5-flash")

browser_session = BrowserSession(
    keep_alive=True, 
    headless=False,
    wait_for_network_idle_page_load_time=3.0,
    allowed_domains=['*.producthunt.com', '*'],
    executable_path="C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")

"""
1. Navigate to Product Hunt (intro )
2. Get the Top two Products name and urls from visit site (Speak the names)
3. a for loop to interate through the top two products (using the urls)
4. For each product, click on the product link and explore the product page
5. Brief review on the UI
6. Get the navbar elements with links
7. For each navbar element, click on it and provide a review
8. Speak the reviews of each navbar element
9. Outro
10. Close the browser session


"""


async def main():
    await browser_session.start()
    #agent-1 navigates to Product Hunt
    agent1 = Agent(
            task="Navigate to https://producthunt.com ",
            llm=llm,
            browser_session=browser_session
            )
    await agent1.run() 

    speak("Hey everyone, welcome back to the channel! Today, we’re diving into the world of cutting-edge AI . I’m checking out the most talked-about tools trending right now on Product Hunt. Let’s jump in and see what’s making waves in the AI space!")

    #agent-2 searches for top two products on Product Hunt
    agent = Agent(
        task="""From the current Product Hunt page, extract the names of the top two listed products. For each product, also extract the URL behind the 'Visit Website' link.Return the result in the following JSON format: 
        [
  {
    "product_name": "Product A",
    "visit_website_url": "https://..."
  },
  {
    "product_name": "Product B",
    "visit_website_url": "https://..."
  }
]
```""",
        llm=llm,
        browser_session=browser_session,
        controller=controller1
    )
    history = await agent.run()
    res = history.final_result()
    print(res)
    print(res)
    urls = []
    if res:
        parsed: Posts = Posts.model_validate_json(res)
        if parsed.posts:
            first_post = parsed.posts[0]
            title1 = first_post.post_title
            urls.append(first_post.post_url)
            second_post = parsed.posts[1]
            title2 = second_post.post_title
            urls.append(second_post.post_url)
        speak(f"The top products of the day are {title1} and {title2}. Let's take a closer look!")
        print("urls are: ",urls)

    else:
        print('No result')
    async def visit_url(url):    
        agent2 = Agent(
            task=f"go to {url}, from the result click on the 'visit website' option on the page ",
            llm=llm,
            browser_session=browser_session
        )
        casual_ui_prompt = """
WEBSITE UI REVIEW STYLE:
- Give short, casual opinions like you're showing a friend a cool website
- Use expressions like "Oh wow!", "This looks...", "I love how...", "The design is..."
- Keep it brief - just 2-3 sentences max
- Focus on first impressions and overall vibe
- Use everyday language, not design jargon
- Be enthusiastic and conversational
- Examples of good responses:
  * "Oh look at this UI! It's super clean and modern, really professional looking!"
  * "Wow, this website has such a sleek design! The colors are really nice and everything feels organized."
  * "This looks pretty cool! The layout is simple but effective, very user-friendly."
"""    
        await agent2.run()
        agent6 = Agent(
            task="give me a quick casual comment about the UI",
            llm=llm,
            browser_session=browser_session,
            extend_system_message=casual_ui_prompt
        )
        history = await agent6.run()
        res = history.final_result()
        speak(res)    
        

    await browser_session.close()



if __name__ == "__main__":
    asyncio.run(main())
   


