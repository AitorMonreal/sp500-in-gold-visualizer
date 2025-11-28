# Deployment and Automation Guide

This guide explains how to host your "S&P 500 Priced in Gold" website for free using **GitHub Pages** and automate daily data updates using **GitHub Actions**.

## 1. Hosting on GitHub Pages

GitHub Pages is a static site hosting service that takes HTML, CSS, and JavaScript files directly from a repository on GitHub and publishes a website.

### Steps:

1.  **Create a GitHub Repository**:

    - Go to [GitHub.com](https://github.com) and create a new public repository (e.g., `sp500-gold-visualizer`).

2.  **Push Your Code**:

    - Initialize git in your project folder if you haven't already:
      ```bash
      git init
      git add .
      git commit -m "Initial commit"
      ```
    - Link your local folder to the GitHub repo:
      ```bash
      git remote add origin https://github.com/<YOUR_USERNAME>/sp500-gold-visualizer.git
      git branch -M main
      git push -u origin main
      ```

3.  **Enable GitHub Pages**:

    - Go to your repository **Settings** > **Pages**.
    - Under **Source**, select `Deploy from a branch`.
    - Under **Branch**, select `main` and `/ (root)`.
    - Click **Save**.

4.  **View Your Site**:
    - GitHub will provide a URL (usually `https://<YOUR_USERNAME>.github.io/sp500-gold-visualizer/`).
    - It might take a minute or two to go live.

## 2. Automating Daily Updates

I have included a GitHub Actions workflow file in your project at `.github/workflows/daily_update.yml`. This script tells GitHub to run your `download_data.py` script every day.

### How it works:

1.  **Schedule**: The script runs automatically at 00:00 UTC every day.
2.  **Environment**: It sets up a Python environment and installs dependencies from `requirements.txt`.
3.  **Execution**: It runs `python download_data.py` to fetch the latest data.
4.  **Update**: If `data.json` changes (i.e., new data is added), it automatically commits the new file and pushes it back to your repository.
5.  **Live Update**: Since GitHub Pages serves the files from your repository, your website will automatically show the updated chart within a few minutes of the script finishing.

### Verification:

- You can check the **Actions** tab in your GitHub repository to see the workflow running.
- You can also manually trigger the update by going to **Actions** > **Daily Data Update** > **Run workflow**.
