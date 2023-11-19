# Scrapping Task

## Getting Started

This project involves web scraping tasks using Python 3.9. Follow the steps below to set up and run the scraping scripts:

Make sure you have Python 3.9 installed on your system.
Run the following commands in your terminal:

```
chmod +x setup.sh
./setup.sh

```

## About

Scrape following urls and extract only PDPs from them:

- https://foreignfortune.com 
- https://www.lechocolat-alainducasse.com/uk/ (only UK based products)
- https://www.traderjoes.com 

Note: For traderjoes, not all the products are expected. 20-30% works. Plus point on extracting 70% and above.

### Usage permitted:

- Python 3.x and above
- For basic downloading: requests, urllib
- For JS rendering: requests-html, selenium, pyppeteer
- For HTML parsing: beautifulSoup4, parsel
- For JSON parsing: json
- For string patterns: regex, python inbuilt string functionalities
- Any other, as per requirement




### Python Task

- Create a validation class in python to validate the output of the above scraping tasks

For example:
- Sale price is less than or equals to original price
Title, product_id, model_id etc, are mandatory fields
- Each variant (model) has images and their respective prices

Create as many as validation rules as you can.

