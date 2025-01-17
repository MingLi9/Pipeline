# Gemini AI bot

This folder is for the AI bot using Gemini's LLM.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)

## Overview

The program is using the free version of Google's Gemini large language model with a limited amount of tokens and requests as follows:
- 15 RPM (requests per minute)
- 1 million TPM (tokens per minute)
- 1,500 RPD (requests per day)
In order to have access to real time information gathering, the chatbot API has been combined with SerpApi for google search functionality.

## Prerequisites

- Python 3.10+
- Pip

## Setup Instructions

### Step 1: Clone the Repository


```bash
git clone https://github.com/fuas-dverse/group.git
cd group/gemini
```

### Step 2: Install libraries from Google and SerpApi

Highly suggested to build a virtual envrionment in which you install the requirements to run the application

1. **Run the following commands** in the terminal:
  - python -m venv venv
This creates your virtual environment

then activate with (Mac/Linux):
  - source venv/bin/activate
or on Windows:
  - .venv\Scripts\activate

And finally install the required libraries
  - pip install google-generativeai
  - pip install serpapi
  - pip install dotenv

2. **Run the application**:
  You are able now to run gemini.py and interact with the bot.
