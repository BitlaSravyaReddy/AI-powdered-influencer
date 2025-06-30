# Convert ele list to a human-readable string
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
from pathlib import Path
import asyncio
from typing import List
from browser_use import Agent, BrowserSession, Controller
from pydantic import BaseModel


#from langchain.schema import SystemMessage, HumanMessage
load_dotenv()


class Element(BaseModel):
	text: str
	link: str

class Navbar(BaseModel):
	elements: List[Element]
	
controller=Controller(output_model=Navbar)    

# Initialize the model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key="AIzaSyB3bTFSbph48oMQXTohSI9VnzkCrL8LUVc")


browser=BrowserSession(
    headless=True,
	keep_alive=True,
	wait_for_network_idle_page_load_time=3.0,
    allowed_domains=['*.producthunt.com', '*'],
    executable_path=Path('C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe')  # ✅ wrap in Path

)

navbar_str = ['Pricing', 'testiomonals', 'FAQ', 'Try for free now']

navbar_review_prompt = f"""
You're a friendly and casual product reviewer. You're currently visiting a product's website each navbar section.

On this website, you will explore each section linked in the navbar. Visit each one and provide your thoughts.
Now you have to visit {Element}

Your task:
- Try clicking on the navbar element {Element}(if clickable).
- For the section that opens, observe the content on the result page and take note of any key points.
- Give a short, friendly review of what the section is about and how it fits into the overall product experience.
- Use a natural tone, as if you're speaking to a friend while exploring the site.
- Keep each review 2-3 sentences.
- If an element doesn't open or shows a login page, you can skip it or mention that politely.

Output format:
[Element Name]: Your friendly review here.

Example:
Pricing: Looks like they have a clear pricing structure — love how simple the plans are laid out! with a free trial option, which is great for new users.
Features: Oh wow, this (section name) really highlights the core tools well. Very visual and user-friendly.
"""
async def main():
    await browser.start()
    extra_prompt="""
Return all clickable elements (e.g., buttons, links, dropdowns) that navigate to other pages.

Provide the result in **strict JSON format**, where each element is represented as an object with:


IMPORTANT:
If you encounter a dropdown menu, hover on it to reveal its items, and include those in the JSON as well.

- "label": the visible text
- "url": the URL to navigate to
- "children" (optional): a list of items if it's a dropdown

Example format:
[
  {
    "label": "Open main menu"
    "url": "https://neura-app.com/#menu"
  },
  {
    "label": "Product",
    "url": "https://neura-app.com/#product",
  },
]

Only return the JSON list. Do not add explanations or extra text.
"""

    agent= Agent(
        task="Go to 'https://neura-app.com/' ",
        llm=llm,
        browser_session=browser,
        # extend_system_message=extra_prompt
        # controller=controller
    )
    await agent.run()
    # elements = []
    # for item in res:
    #     print(type(item))
    #     label = item.get("label")
    #     elements.append(label)
    # print(elements)

    # element = []
    # for ele in res:
    #     element.append(ele)
    # print("the elements of navbar are:", element)	
    # await browser.kill() 
    # # navbar_str = []
    # if res:
    #     parsed: Navbar = Navbar.model_validate_json(res)
    #     if parsed.elements:
    #         for ele in parsed.elements:
    #             navbar_str.append(ele.text)
    # print("navbar strings are",navbar_str)      
    async def get_review(Element:str):
        agent = Agent(
          task=f"""
You're a friendly and casual product reviewer. You're currently visiting a product's website each navbar section.

On this website, you will explore each section linked in the navbar. Visit each one and provide your thoughts.
Now you have to visit {Element}

Your task:
- Try clicking on the navbar element {Element}(if clickable).
- For the section that opens, observe the content on the result page and take note of any key points.
- Give a short, friendly review of what the section is about and how it fits into the overall product experience.
- Use a natural tone, as if you're speaking to a friend while exploring the site.
- Keep each review 2-3 sentences.
- If an element doesn't open or shows a login page, you can skip it or mention that politely.

Output format:
[Element Name]: Your friendly review here.

Example:
Pricing: Looks like they have a clear pricing structure — love how simple the plans are laid out! with a free trial option, which is great for new users.
Features: Oh wow, this (section name) really highlights the core tools well. Very visual and user-friendly.
""",
          llm=llm,
          browser_session=browser,
          
        )
        history = await agent.run()
        return history.final_result()
    for element in navbar_str:
        review = await get_review(element)
        print(f"{element}: {review}")
        # speak(f"{element}: {review}")  # Uncomment if you want to use TTS




asyncio.run(main())