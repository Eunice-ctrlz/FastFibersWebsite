# FAST FIBERS WEBSITE

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
[![Python: 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-Running-green)](https://www.uvicorn.org/)

---

## PROJECT GOAL AND PROBLEM SOLVED
PROJECT GOAL:


### The Problem
FastFibersWebsite is a responsive, fast-loading website created to provide an online presence for Fast Fibres, a local IT services company.
The website is designed to showcase services, provide contact information, and enhance credibility, enabling potential clients to easily access information about WiFi and CCTV installation services.

### The Solution
Before FastFibersWebsite, Fast Fibres had limited online visibility, which restricted client reach and business growth. The website addresses this by:

1. Acting as a central hub for all services offered
2. Allowing clients to quickly view services and contact the business
3. Delivering a fast and mobile-friendly experience
4. Helping the business build trust and professionalism online


##  Features  
This API supports the following core functionalities:

Responsive design: Works seamlessly on desktop and mobile devices
Fast load times: Fully loads in ~464ms
Service showcase: Detailed sections for WiFi and CCTV installation
Contact information: Clear, accessible contact details for clients
Professional layout: Clean, modern, and easy-to-navigate interface

## Tech Stack

| Category                 | Technology                 | Purpose                                                    |
|--------------------------|---------------------------|-------------------------------------------------------------|
| Backend Framework        | FastAPI                   | High-performance, low-latency API development.              |
| Asynchronous Server      | Uvicorn                   | ASGI server for serving the FastAPI application.            |
| Database                 | MySQL                     | Relational database for storing service data and records.   |
| ORM / Database Toolkit   | SQLAlchemy                | Python SQL toolkit and Object Relational Mapper.            |
| Frontend                 | HTML, CSS, JavaScript     | User interface, responsive and interactive design.          |
| Deployment               | Railway                   | Cloud platform for backend hosting and continuous deployment.|
| Frontend Hosting         | GitHub Pages              | Hosting static frontend files for public access.            |
| Configuration Management | pydantic-settings         | Secure, type-checked environment variable management.       |


---

## 🔗 Live Demo & Documentation

| Resource | Link | Notes |
| **Live API Endpoint** | fastapi-production-1d3f.up.railway.app | The current health check response is: {"status":"online","message":"Payment API is running","version":"1.0.0"} |
| **API Documentation (Swagger/OpenAPI)** | fastapi-production-1d3f.up.railway.app/docs | Auto-generated interactive documentation for all endpoints. |
| **Video Walkthrough** | [Link to your 2-minute YouTube/Vimeo Demo] | Recommended viewing for a quick overview of features. |

---

## ⚙️ Local Setup and Installation
### Prerequisites
- Python 3.10+ – for running the backend
- MySQL – for the database
- Git – for cloning the repository
- Node.js / npm (optional) – if you plan to run frontend build tools

### Steps

1.  **Clone the Repository:**
  git clone https://github.com/Eunice-ctrlz/FastFibersWebsite.git
  cd FastFibersWebsite


2.  **Install Dependencies:**
    ```bash
    # If using poetry
    poetry install 
    
    # OR if using pip
    pip install -r requirements.txt 
    ```

3.  **Set Environment Variables:*
   DB_HOST=localhost
  DB_USER=your_mysql_user
  DB_PASSWORD=your_mysql_password
  DB_NAME=fastfibers_db


5.  **Run Migrations (if applicable):**
   ```bash
    python manage.py  # or the script you use to create tables


7.  **Start the Server:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

---

## Lessons Learned & Technical Challenges

This section highlights the challenges faced during development and the lessons learned, useful for interviews and demonstrating a growth mindset.
*Challenge 1*: Managing Environment Variables Securely
Solution: We used pydantic-settings to load configuration from environment variables, avoiding hardcoded secrets. This improved security and made deployment on Railway safer and more reliable.
*Challenge 2*: Connecting Frontend to Backend APIs
Solution: Ensured that frontend JavaScript API calls correctly pointed to the Railway-hosted backend endpoints, handling CORS issues and asynchronous requests.
*Challenge 3*: Database Integration with FastAPI
Solution: Used SQLAlchemy ORM to manage MySQL database connections and sessions efficiently, ensuring consistent and reliable CRUD operations.
*Challenge 4*: Optimizing Website Performance
Solution: Minimized HTTP requests, compressed images, and optimized CSS/JS, achieving ~464ms load time and high Lighthouse performance scores.
Learnings:
1. Learned best practices for full-stack project structure combining frontend and backend.
2. Gained experience in deployment workflows on GitHub Pages and Railway.
3. Improved understanding of asynchronous programming with FastAPI and Uvicorn.
Next steps: Explore automated testing and CI/CD pipelines to further enhance deployment and maintainability.

## Contribution & Contact

Contributions, issues, and feature requests are welcome! Feel free to check the Issues Page.

* **Author:** EUNICE WAIRIMU MUTURI
* **LinkedIn:** https://www.linkedin.com/in/eunice-muturi-7023b6342/
* **Email:** emuturi339@gmail.com

