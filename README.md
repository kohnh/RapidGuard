# [RapidGuard]


A brief one- or two-sentence tagline about your project.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Setup Guide](#setup-guide)
- [User Guide](#user-guide)
- [Features](#features)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Project Overview

**[RapidGuard]** is a hackathon project designed to [explain the main purpose]. It solves the problem of [describe the problem] by [explain your solution briefly].

### Key Points

- **What it does:**  
  Brief description of your project’s core functionality.
  
- **Problem solved:**  
  Outline the challenge or need that your project addresses.
  
- **Why it matters:**  
  Explain the impact of your solution or how it benefits users.

---

## Setup Guide

Follow these step-by-step instructions to get the project up and running on your local machine.

### Prerequisites

- **Git:** [Download and install Git](https://git-scm.com/downloads)
- **Next.js:** [Download and install Node.js and npm](https://nodejs.org/en/download/)
- **Python:** [Download and install Python 3](https://www.python.org/downloads/)
- **Virtual Machine:** AWS EC2 Instance [t2.medium and above] (or any other cloud provider)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kohnh/RapidGuard.git
   cd drms2
    ```

2. **Create a virtual environment:**

   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies for backend:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install the dependencies for frontend:**

   ```bash
   cd ../frontend
   npm install
   ```

5. **Configure the environment:**

   Create .env file in the backend folder and add the following:

   ```bash
   cd ../backend
   OPENAI_API_KEY="your_openai_api_key"
   HOST_IP_ADDRESS="your_virtual_machine_ip_address"
   ```

6. **Download NX Witness**

   ```
   <insert download from where, how to set it up>
   <insert how to set up the camera>
   <insert how to add in the ML model>
   ```

7. **Start the backend server:**

   ```bash
   python -m gunicorn -k eventlet --workers 1 --bind 0.0.0.0:5000 main:app
   ```

8. **Start the frontend server:**

   ```bash
    cd ../frontend
    npm run dev
    ```
    Check the console to verify that socket connection is established.
    You should see a message like this:
    ```
    Socket connected with id: WqBZsZsGN0wLN0cMAAAB
    ```

9. **Access the application:**

    Go to web pages and access the application at `http://<HOST_IP_ADDRESS>:3000`.


---

## User Guide
Here is a brief guide on how to use the application.

### How to use the application