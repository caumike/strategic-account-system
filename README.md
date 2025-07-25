# Strategic Account Management System - by Startup-IQ

This Streamlit application provides an AI-powered analysis of a target sales account. It gathers live data from the web, identifies a key sales opportunity, and maps a path to relevant contacts using the user's exported LinkedIn network.

## How to Run Locally

1.  **Set up your environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Download NLP models (one-time setup):**
    ```bash
    python -m textblob.download_corpora
    ```
4.  **Run the application:**
    ```bash
    streamlit run main-app.py
    ```

## How to Export Your LinkedIn Connections

This application requires you to upload a `Connections.csv` file.

1.  Log in to LinkedIn.
2.  Click **Me** > **Settings & Privacy**.
3.  Go to **Data privacy** > **Get a copy of your data**.
4.  Select **"Want something in particular?"** and check the **Connections** box.
5.  Click **Request archive**. LinkedIn will email you a download link.
6.  Download and unzip the file. You will find `Connections.csv` inside.
