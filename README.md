# [RapidGuard - Your actionable disaster response and management solution](https://github.com/kohnh/RapidGuard)


[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Contributors](https://img.shields.io/badge/Contributors-4-blue.svg)](github.com/kohnh/RapidGuard/graphs/contributors)

RapidGuard is an AI-powered disaster response system that delivers real-time hazard detection, dynamic emergency guidance, and interactive, context-aware updates, even when conventional analytics fall short under pressure.

## Table of Contents

- [Project Overview](#project-overview)
- [Setup Guide](#setup-guide)
- [User Guide](#user-guide)
- [Architecture](#architecture)
- [Contributing](#contributing)


## Project Overview

RapidGuard is a Nx Venue Innovation Hackathon  project designed to revolutionize disaster management in high-traffic venues by leveraging advanced AI for real-time hazard detection and integrating generative language models (LLMs) to provide actionable emergency response strategies. Traditional systems tend to be analytics-based and offer little in the way of immediate, practical steps—especially in rare, complex, and rapidly evolving disaster scenarios. Moreover, in high-pressure situations, it is extremely challenging for operators to derive effective solutions solely from static fire management SOPs, particularly when CCTV systems may have blindspots and staffing issues (e.g., a missing security guard).

RapidGuard addresses these challenges by continuously monitoring live CCTV feeds using a self-trained machine learning model built with Teachable Machine for fire detection. Upon identifying a potential hazard, it automatically activates a Disaster Response and Management System (DRMS) that uses LLMs to generate detailed, real-time emergency response plans. Furthermore, operators can interact directly with the LLM via a chat interface—allowing them to provide additional context such as updated fire conditions or on-the-ground insights. This extra context is automatically extracted from the user's input without requiring them to specify whether they are asking a question or merely adding unseen context from the CCTV feeds. The LLM then continuously refines and updates the response plan, ensuring that actionable guidance remains aligned with the evolving situation.

### Key Points

- **What it does:**  
  RapidGuard continuously monitors live CCTV feeds using a self-trained machine learning model built with Teachable Machine for fire and smoke detection. When a potential hazard is detected, it activates a DRMS that leverages LLMs to generate an initial emergency response plan and then dynamically updates the plan based on real-time changes in the situation. Operators can interact with the LLM via a chat interface, and any additional context provided is automatically integrated to refine the guidance.
  
- **Problem solved:**  
  Traditional surveillance systems and analytics-based solutions offer data without immediate, actionable steps, making it difficult for operators to respond effectively under stress. RapidGuard bridges this gap by automating hazard detection and translating complex SOPs into practical, adaptive instructions—even when blindspots or staffing issues occur.
  
- **Why it matters:**  
  By transforming raw analytics into dynamic, actionable emergency strategies and allowing for interactive, real-time updates, RapidGuard significantly improves situational awareness and decision-making during crises. This not only optimizes resource allocation and enhances safety in high-traffic venues but also ensures that on-ground input is seamlessly incorporated into evolving emergency plans, ultimately safeguarding lives and property.

### Demo Video

[![Watch the video](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)

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

6. **Download and Set Up NX Witness**

   **Install NX Witness:**
   1. Download and install **NX Witness** from [this page](https://nxvms.com/download/releases/linux).
   2. Open **NX Witness** and log in to your server using your credentials. If this is your first time connecting, enter the **server login details**.
   3. Log in to **NX Cloud** by clicking the cloud icon in the top-right corner.

   **Deploy the Fire Detection Model via NX AI Manager:**
   > Ensure the **NX Witness server** is set up before proceeding.

   1. Select the **camera** where you want to deploy the AI model.
   2. **Right-click** on the camera and select **Camera Settings**.
   3. Navigate to the **Plugins Tab** and select **NX AI Manager**.
   4. Activate **NX AI Manager**:
      - Toggle the activation switch (this may take a few minutes).
      - Change **Camera Stream** to **Secondary**.
      - Ensure **Device Active** is enabled.
   5. Deploy the **fire detection model**:
      - Click **Manage Device** and wait for the data to load.
      - Select **Add a new pipeline** and choose the desired model.
      - Click **"Add to CAMERA_NAME pipeline"** and wait for deployment.
      - *(Optional)* Add a **post-processing function** if needed.
   6. Click **Apply**, then **OK** to save changes.

   **Configure NX Witness for Event Notification (POST Request):**
   1. Select the **camera** running the AI model.
   2. **Right-click** on the camera and select **Camera Rules**.
   3. Add a **new camera rule**:
      - Set the **URL** to the **IP address of the device running `server.py`**.
      - Adjust the **POST request frequency** as needed.
      - <img src="images_for_README/setting_camera_rules.png" alt="Camera Rules" style="margin-right: 10px;" />
   4. Click **Apply**, then **OK** to confirm the settings.

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

    Go to web pages tab on NX Witness and access the application at `http://<HOST_IP_ADDRESS>:3000`.


---

## User Guide
Here is a brief guide on how to use the application.

### How to use the application


## Architecture
Here is a high-level overview of the project architecture.

![architecture diagram](./images_for_README/architecture_diagram.png)


## Contributing
[![Contributors](https://img.shields.io/badge/Contributors-4-blue.svg)](https://github.com/kohnh/RapidGuard/graphs/contributors) -->

<a href="https://github.com/thebadone231" target="_blank">
  <img src="https://github.com/thebadone231.png?size=100" alt="Chen Haoli" style="margin-right: 10px;" />
</a>
<a href="https://github.com/euzhengxi" target="_blank">
  <img src="./images_for_README/blank-profile-picture.png" alt="Eu Zheng Xi" style="margin-right: 10px; width: 100px; height: 100px; />
</a>
<a href="https://github.com/ong-ck" target="_blank">
  <img src="https://github.com/ong-ck.png?size=100" alt="Ong Chuan Kai" style="margin-right: 10px;" />
</a>
<a href="https://github.com/kohnh" target="_blank">
  <img src="https://github.com/kohnh.png?size=100" alt="Koh Ngiap Hin" />
</a>