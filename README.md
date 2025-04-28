# Unified Price Comparison Platform: One-step solution for smart shopping

The **Unified Price Comparison Platform** is a web application that helps users compare product prices between major E-commerce websites and grocery stores. The platform allows users to input a product name and fetch the **Images**, **Links**, and **Prices** from:

- **E-commerce**: Flipkart and Amazon
- **Groceries**: JioMart and Zepto

The backend is built with **Python** using **Flask**, while web scraping is done using **BeautifulSoup** and **Selenium**.

## Features

- User-friendly web interface to enter the product name and fetch prices along with links and Images.
- Scrapes Information from Flipkart, Amazon ,JioMart and Zepto websites.
- Displays the fetched information on the web page.

## Prerequisites

- Python 3.x
- Flask
- BeautifulSoup
- Selenium
- Chrome WebDriver (for Selenium)

## How to Run

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/Akhilesh56Mangalapalli/Unified-Price-Comparison-Platform
   ```

2. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

3. Download the appropriate Chrome WebDriver for your operating system and place it in your system's PATH.

4. Run the Flask application:

   ```
   python app.py
   ```

5. Open the application in your web browser:

   - Access the application at http://127.0.0.1:5000/ after starting the Flask server.

   Choose your domain:

   - Select E-commerce to compare prices from Flipkart and Amazon.

   - Select Groceries to compare prices from JioMart and Zepto.

   Enter the product name:

   - Type the product name in the input field.

   Click "Scrape Prices":

   - After submitting the product name, the application will scrape prices from the selected domain(s) and display the results on the page, showing the product images, prices, and links from the respective platforms.

## How It Works

The Flask application (app.py) serves as the backend of the web application. When the user submits a product name through the web form, the backend fetches the product prices from the selected websites using web scraping techniques.

E-commerce (Flipkart & Amazon):

   - The scrape_flipkart function uses BeautifulSoup to scrape the Flipkart website and obtain the product price.

   - The scrape_amazon function uses Selenium to render the Amazon website (since it's dynamically loaded) and then uses
     BeautifulSoup to extract the product price from the rendered page.

Groceries (JioMart & Zepto):

   - The scrape_jiomart function uses BeautifulSoup to scrape JioMart and fetch the product price and other details.

   - The scrape_zepto function uses BeautifulSoup to scrape Zepto and extract the product price along with related
     information.

The scraped prices and data are then sent back to the frontend and displayed on the web page in a user-friendly format.

## Folder Structure

```
Unified Price Comparison Platform/
│
├── app.py              # main Python backend file (Flask)
│
├── static/styles/      # Folder containing CSS styles
│   └── mainpage.css    # Styling for web pages
│
├── templates/          # HTML templates folder 
│   ├── index.html      # Home page
│   ├── ecommerce.html  # E-commerce price comparison page
│   └── groceries.html  # Grocery price comparison page
│
├── requirements.txt    # List of required Python packages
│
└── README.md           # Documentation for the project (this file)

```

`app.py:` Flask application and web scraping functions.

`mainpage.css:` CSS file for styling the frontend (located inside static/styles/).

`index.html:` Home page for product input (inside templates/).

`ecommerce.html:` E-commerce price comparison page (inside templates/).

`groceries.html:` Grocery price comparison page (inside templates/).

`requirements.txt:` List of required Python packages.

`README.md:` Project documentation.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

Please note that web scraping might violate the terms of service of websites. Use this application responsibly and ensure compliance with the terms and conditions of the websites you scrape. The authors of this project are not responsible for any misuse or violations.
