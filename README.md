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

    - Python 3.x
    - Docker
    - Docker Compose

2.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd bug-recon-ai
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Build the Docker containers:**
    ```bash
    docker-compose build --profile build-only
    ```

## Usage

Run the application from the terminal:
```bash
python app/main.py <domain>
```


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
