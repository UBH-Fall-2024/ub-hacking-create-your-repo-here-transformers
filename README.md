[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/_U2QbDVP)

# Interview AI

## Table of Contents

1. [**Introduction**](#introduction)
2. [**Features**](#features)
3. [**Installation**](#installation)
4. [**Environment Variables**](#environment-variables)
5. [**Usage**](#usage)
6. [**Example**](#example)
7. [**Project Architecture**](#project-architecture)
8. [**Tech Stack**](#tech-stack)
9. [**Contributing**](#contributing)
10. [**License**](#license)

---

## Introduction

**Interview AI** is a tool designed to aid interviewers by dynamically generating relevant follow-up questions based on the candidate's responses. This project ensures that the interviewer never runs out of insightful questions, keeping the interview flowing smoothly and enhancing its depth.

## Features

- **Real-Time Follow-Up Questions:** Using AI-powered models, this app listens to interview responses, converts them from speech-to-text, and suggests contextually relevant follow-up questions in real-time.
- **Large Language Model Integration:** Hosts an LLM for text processing, accessible via a Docker container.
- **Streamlit Interface:** Interviewers can view generated questions and other insights in an intuitive Streamlit dashboard.
- **Docker Deployment:** Containerizes the model and deploys it using Docker.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/UBH-Fall-2024/ub-hacking-create-your-repo-here-transformers.git
   
2. Set up the Docker environment:
   ```bash
   docker build -t speech-to-text
   
3. Start the Docker container:
   ```bash
   docker run -p 8000:8000 speech-to-text
   
4. Install dependencies for local Python development (optional):
   ```bash
   pip install -r requirements.txt

### Environment Variables

- MODEL_PATH: Path to the Vosk model for speech-to-text recognition.
- LOG_PATH: Directory path for logging the fails index.
- Update these in a .env file or within Docker environment variables as needed.

Usage
- Start the Service: Run the Docker container as described in the Installation section.
- Make Requests: Access the service API at http://localhost:8000 for speech-to-text transcription.

- Example transcription request and response:
```bash
curl -X POST -F http://localhost:8000/ask

### Project Architecture

(The architecture diagram visually represents the project's workflow and components.)

- **Speech-to-Text Conversion:** Captures the candidate’s spoken answers and converts them into text format.
- **Vector Database:** Stores candidate responses and retrieves similar past responses to generate follow-up questions.
- **LLM Model:** Processes responses and suggests relevant questions based on context.
- **Streamlit Interface:** Displays the generated questions to the interviewer in real-time.
- **S3 Storage:** Used to store audio as text data as part of the interview logs.

### Tech Stack

- **Speech-to-Text:** Vosk
- **Vector Database:** FAISS
- **Large Language Model:** Llama-3.2-3B-Instruct
- **UI Framework:** Streamlit
- **Cloud Storage:** Amazon S3
- **Containerization:** Docker

