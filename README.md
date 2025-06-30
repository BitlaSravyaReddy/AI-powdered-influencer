# AI-Powdered Influencer 🎥🤖

## Overview

**AI-Powdered Influencer** is a voice-driven browser automation system that acts like a human YouTuber reviewing new tech products on [Product Hunt](https://www.producthunt.com/). It uses a Large Language Model (LLM) to analyze product pages, navigate their UI, explore navigation bars, and then **speak natural-sounding reviews** using TTS. All browser activity is automated using Brave via Playwright.

This project is ideal for creating automated review content or testing the UX of product websites.

---

## Table of Contents

1. [Features](#features)
2. [Demo Flow](#demo-flow)
3. [Project Structure](#project-structure)
4. [Requirements](#requirements)
5. [Installation](#installation)
6. [Environment Setup](#environment-setup)
7. [Running the Project](#running-the-project)
8. [Model Evaluation Insights](#model-evaluation-insights)
9. [Customization](#customization)
10. [License](#license)

---

## Features

- 🌐 **Brave Browser Automation** using `browser-use` and Playwright
- 🔎 **Top Product Discovery** from Product Hunt
- 🧠 **LLM-Powered Reviews** using Gemini 2.0/2.5 or OpenAI GPT
- 🗣️ **Speech Generation** with `pyttsx3` for real-time narration
- 🔗 **Navbar Exploration** and UI evaluation
- 🎙️ **Human-like Voice Output** for each step
- 🧾 **Structured Output** using `pydantic`

---

## Demo Flow

The project executes the following steps automatically:

1. **Navigate** to [Product Hunt](https://producthunt.com)
2. **Extract** names and URLs of the top 2 products
3. For each product:
   - Visit the product page
   - Review the **UI and layout**
   - Identify navbar elements and their links
   - Click each navbar link
   - Provide spoken feedback for each section
4. **Speak** reviews at each step
5. Close the browser session

---

## Project Structure

📁 BitlaSravyaReddy/
├── README.md
├── demo.py
├── final.py
├── influencer_video_1750429767.mp4
├── influencer_video_1750431069.mp4
├── main.py
├── main1.py
├── navbar-reviw.py
├── requirements.txt
└── reviewing.py


---


---

## Requirements

- **Python**: 3.13.3
- **Browser**: Brave (must be installed)
- **LLM**: Gemini 2.0 Flash / 2.5 Flash / OpenAI GPT-4
- **Python Libraries**:
  - `browser-use==0.2.5`
  - `pyttsx3`
  - `pydantic`
  - `openai` or `google-generativeai`
  - `python-dotenv`

---

## Installation

1. **Clone the repository**:

git clone https://github.com/yourusername/ai-powdered-influencer.git
cd ai-powdered-influencer


2. Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate



3. Install the dependencies:
   
pip install -r requirements.txt



4. Environment Setup
Create a .env file in the root folder with your LLM API key:

# For Gemini
GEMINI_API_KEY=your_gemini_api_key

# OR for OpenAI
OPENAI_API_KEY=your_openai_api_key

## Running the Project
Simply run:

python main.py

The bot will:

1. Open Brave browser,

2. Fetch and visit top products,

3. Analyze each section,

4. Speak human-like feedback,

5. Close after completing all tasks.



## Model Evaluation Insights


According to our internal research, various open-source local LLMs were tested to automate and narrate browser sessions. However, most models failed to fully comprehend or execute the multi-step interaction flow. Here's a summary:

| Model Name              | Observation / Limitation                                      |
| ----------------------- | ------------------------------------------------------------- |
| **DeepSeek Coder 6.7B** | Hallucinates frequently; unsuitable for reliable use          |
| **LLaMA 3.1 7B**        | Gets stuck in search bar loop; poor browser understanding     |
| **Qwen2 7B**            | Inconsistent task performance                                 |
| **Yi 9B**               | Loops on `example.com` tab; blank navigation issues           |
| **LLaMA (Groq)**        | Unable to maintain logical navigation                         |
| **Mistral (latest)**    | Fails to understand task; stuck in infinite loop              |
| **Qwen 2.5 14B**        | Best among local models; still slow and occasionally confused |

✅ Conclusion: Cloud-based models like Gemini 2.0 Flash / 2.5 Flash offer superior task comprehension and contextual consistency, making them more suitable for this browser automation task.

