from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
#import dotenv
from pathlib import Path
import asyncio
from typing import List
from browser_use import Agent, BrowserSession, Controller
from pydantic import BaseModel
import pyttsx3

from langchain.schema import SystemMessage, HumanMessage


# Initialize the model
#llm = ChatOpenAI(model="gpt-4o")

def generate_narration(context: str, task: str) -> str:
    messages = [
        SystemMessage(content="You're a friendly and helpful tech influencer who narrates your browsing journey."),
        HumanMessage(content=f"""\
You are currently doing the following task: **{task}**

Here is some context or data on the screen:
{context}

Generate a natural-sounding English sentence or two that you'd say aloud as a product reviewer.
""")
    ]
    response = llm(messages)
    return response.content.strip()


tts = pyttsx3.init()
tts.setProperty('rate', 150)
def speak(text):
        """Speak text using TTS"""
        print(f"🎤 Speaking: {text}")
        tts.say(text)
        tts.runAndWait()

class Post(BaseModel):
	post_title: str
	post_url: str

class Posts(BaseModel):
	posts: List[Post]

class Detail(BaseModel):
	navbar_element : str

class Details(BaseModel):
	titles : List[Detail]

     		
	
controller = Controller(output_model=Posts)  
controller1 = Controller(output_model=Details)  

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key="AIzaSyB3bTFSbph48oMQXTohSI9VnzkCrL8LUVc")

browser=BrowserSession(
    headless=True,
	keep_alive=True,
	wait_for_network_idle_page_load_time=3.0,
    allowed_domains=['*.producthunt.com', '*'],
    executable_path=Path('C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe')  # ✅ wrap in Path

)


async def main():
	await browser.start()
	tasks = "go to producthunt.com and get the names and get the urls from visit website in the page of top two products"

	agent = Agent(
		task=tasks,
		llm=llm,
		browser_session=browser,
		controller=controller
	)

	history = await agent.run()
	
	res = history.final_result()
	print(res)
	urls=[]
	if res:
		parsed: Posts = Posts.model_validate_json(res)
		if parsed.posts:
			first_post = parsed.posts[0]
			title1= first_post.post_title
			urls.append(first_post.post_url)
			second_post = parsed.posts[1]
			title2 =second_post.post_title
			urls.append(second_post.post_url)
		speak(f"the top products of the day are {title1} and {title2}")

	else:
		print('No result')
		
	async def visit_url(url):	
			agent2=Agent(
				task=f"go to {url}, from the result click on the 'visit website' option on the page ",
				llm=llm,
				browser_session=browser
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
			agent6= Agent(
				task="give me a quick casual comment about the UI",
				llm=llm,
				browser_session=browser,
				extend_system_message=casual_ui_prompt
				
			)
			history= await agent6.run()
			res=history.final_result()
			speak(res)
			agent5= Agent(
				task="get the elements on the navbar",
				llm=llm,
				browser_session=browser,
				controller=controller1
			)
			history= await agent5.run()
			res = history.final_result()
			print(res)
			ele=[]
			if res:
				parsed: Details = Details.model_validate_json(res)
				for opt in parsed.titles:
					ele.append(opt.navbar_element)
				speak(f"the navbar elements are {ele}")	

			else:
				print('No result')
			# agent4= Agent(
			# 	task= "If you can see  and give a review of each of them",
			# 	llm=llm,
			# 	browser_session=browser
			# )
			# await agent4.run()
			
	for url in urls:
		print(url)
		await visit_url(url)
	
	await browser.kill()	
		
	




		
	

asyncio.run(main())    