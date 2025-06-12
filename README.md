# Wikipedia Deck

An immersive, swipeable deck for discovering random Wikipedia articles, one at a time. This project is a minimalist reader designed to showcase a fast, modern, and responsive server-driven UI built with Python, Flask, and HTMX.

## Features

-   **Minimalist UI:** A clean, distraction-free interface for reading.
-   **Tap Navigation:** Simply tap the left or right side of the screen to navigate to the previous or next article.
-   **Server-Driven:** Powered by HTMX, keeping the frontend simple and the logic on the server.
-   **Fully Responsive:** A great experience on both desktop and mobile devices.
-   **Deployable:** Ready to be deployed on platforms like Vercel with minimal configuration.

## Tech Stack

-   **Backend:** Python with Flask
-   **Frontend:** HTMX
-- **Styling:** Plain CSS (no frameworks)
-   **API:** Wikipedia REST API

## Running Locally

To run this project on your own machine, follow these steps.

### Prerequisites

-   Python 3.6+
-   `pip` for installing packages

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sh1vananda/wiki-deck.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```

5.  Open your browser and navigate to `http://127.0.0.1:5000`.

## Deployment

This application is configured for easy deployment on Vercel.

1.  Push your code to a GitHub repository.
2.  Import the repository on Vercel.
3.  Add the Flask `SECRET_KEY` as an environment variable in the Vercel project settings.
4.  Deploy! Vercel will automatically use the `vercel.json` and `requirements.txt` files.

---
