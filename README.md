# Bug Recon AI

Bug Recon AI is a web-based tool designed to automate the initial phases of bug bounty reconnaissance. It leverages popular open-source tools to gather information about a target domain, including subdomain enumeration, port scanning, and web technology identification.

## Features

- **Subdomain Enumeration:** Uses Sublist3r to discover subdomains of a target.
- **Port Scanning:** Utilizes Nmap to scan for open ports on the target.
- **Technology Identification:** Employs WhatWeb to identify web technologies.
- **Containerized:** All tools are containerized using Docker for easy setup and execution.

## Technologies Used

- **Backend:** Python, Flask
- **Containerization:** Docker, Docker Compose
- **Scanning Tools:**
  - Nmap
  - Sublist3r
  - WhatWeb

## Setup and Installation

1.  **Prerequisites:**

    - Docker
    - Docker Compose

2.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd bug-recon-ai
    ```

3.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```

## Usage

1.  Once the containers are running, open your web browser and navigate to `http://localhost:5000`.
2.  Enter the target domain in the input field and click "Scan".
3.  The results of the reconnaissance will be displayed on the page.

## Project Structure

```
.
├── app/
│   ├── main.py         # Main Flask application
│   ├── modules/        # Business logic for scanning tools
│   ├── templates/      # HTML templates for the web interface
│   └── utils/          # Utility functions
├── docker/
│   ├── main.Dockerfile # Dockerfile for the main Flask app
│   ├── nmap.Dockerfile
│   ├── sublister.Dockerfile
│   └── whatweb.Dockerfile
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
└── README.md
```
