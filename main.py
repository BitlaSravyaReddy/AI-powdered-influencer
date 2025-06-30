# import asyncio
# from utils.recorder import TimestampedRecorder
# from utils.browser_automation import BrowserAutomation
# from utils.script_generator import ScriptGenerator
# from utils.srt_generator import SRTGenerator
# from utils.tts_generator import TimedTTSGenerator
# from tasks.producthunt_tasks import get_producthunt_tasks
# from config import Config

# async def main():
#     # Initialize components
#     recorder = TimestampedRecorder()
#     browser_automation = BrowserAutomation(recorder)
    
#     print("Starting AI Influencer Pipeline...")
#     recorder.start_recording()
    
#     try:
#         # Get tasks and execute
#         tasks = get_producthunt_tasks()
#         results = await browser_automation.execute_task_sequence(tasks)
        
#         # Generate outputs
#         recorder.save_action_log()
        
#         script_gen = ScriptGenerator('output/logs/action_log.json')
#         script_segments = script_gen.generate_script()
        
#         srt_gen = SRTGenerator(script_segments)
#         srt_gen.generate_srt("output/subtitles/subtitles.srt")
        
#         tts_gen = TimedTTSGenerator()
#         tts_gen.generate_timed_audio(script_segments, "output/audio/narration.wav")
        
#         print("Pipeline completed successfully!")
        
#     except Exception as e:
#         print(f"Error: {e}")
#         recorder.save_action_log()

# if __name__ == "__main__":
#     asyncio.run(main())

#from browser_use import Agent, Controller, ActionResult
# Try importing directly from browser_use if llm submodule does not exist
#from langchain_google_genai import ChatGoogleGenerativeAI
# from browser_use.llm.base import BaseChatModel
# from browser_use.llm import ChatGoogleGenerativeAI
# import asyncio
# from browser_use.llm import ChatGenerativeAI, BaseChatModel

# Initialize the base chat model
#llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key="AIzaSyB3bTFSbph48oMQXTohSI9VnzkCrL8LUVc")


# Use it as the main agent LLM
# agent = Agent(
#     task="Your task here",
#     llm=llm  # Required parameter - base chat model instance
# )

# Create controller with custom functions
# controller = Controller()

# @controller.action('Calculate math expression')
# async def calculate_math(expression: str, page_extraction_llm: BaseChatModel) -> ActionResult:
#     prompt = f"Calculate: {expression}. Return only the number."
#     response = await page_extraction_llm.ainvoke([{"role": "user", "content": prompt}])
#     return ActionResult(extracted_content=f"Result: {response.content.strip()}")

# @controller.action('Fix grammar')
# async def fix_grammar(text: str, page_extraction_llm: BaseChatModel) -> ActionResult:
#     prompt = f"Correct the grammar: {text}"
#     response = await page_extraction_llm.ainvoke([{"role": "user", "content": prompt}])
#     return ActionResult(extracted_content=f"Corrected: {response.content.strip()}")

# # Create agent with custom controller
# async def main():
#         llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key="AIzaSyB3bTFSbph48oMQXTohSI9VnzkCrL8LUVc")

#         agent = Agent(
#             task="Calculate 15 + 27, then fix the grammar in 'Me go to store yesterday'",
#             llm=llm,
#             controller=controller,
#         )

#         # Run the agent
#         history= await agent.run()
#         print(history)
# asyncio.run(main())        
# from browser_use.llm import ChatGoogle
# from browser_use import Agent
# from dotenv import load_dotenv
# import asyncio

# # Load environment variables
# load_dotenv()

# async def main():
#     # Initialize Gemini 2.0 Flash model
#     llm = ChatGoogle(model='gemini-2.0-flash-exp', api_key='AIzaSyB3bTFSbph48oMQXTohSI9VnzkCrL8LUVc')
    
#     # Create agent
#     response = await llm.ainvoke("What is 15 + 17?")
#     print(response.content)  # Should output: 32

#     # Run the agent
    
# if __name__ == "__main__":
#     asyncio.run(main())
from browser_use.llm import ChatGoogle
from dotenv import load_dotenv
import asyncio

load_dotenv()
async def main():
# Use the LLM directly for simple tasks
    llm = ChatGoogle(model='gemini-2.0-flash-exp' , api_key='AIzaSyB3bTFSbph48oMQXTohSI9VnzkCrL8LUVc')

    # For simple text-based tasks, call the LLM directly
    response = await llm.ainvoke("What is 15 + 17?")
    print(response.content)  # Should output: 32    
asyncio.run(main())    