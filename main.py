# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# base_url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"



# page_number=1

# def fetchAndSaveToFile(path,data):
#     with open(path,"w") as f:
#         f.write(data);

# while page_number<=20:
#     # Construct the URL of the current page
#     url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page_number}"
    
#     # Send an HTTP request to the page
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.content, "html.parser")
        
#         # Extract data from the current page
#         # Replace this with the appropriate code to extract your data
#         data = soup.find_all("div", class_="your-data-class")
        
#         # Process and store the data as needed
#         print(data)

#         # Move to the next page
#         page_number += 1
#     else:
#         # Break the loop if the page doesn't exist or other error occurs
#         break



# response=requests.get(base_url,headers=HEADERS)

# # print(type(response.content))

# soup=BeautifulSoup(response.content,"html.parser") #already taken in getProductUrl

# # print(soup)

# product_links=soup.find_all("a",attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}) #already taken in getProductUrl

# actual_link=product_links[0].get('href')  #already taken in getProductUrl
# new_product_link="https://amazon.in" + actual_link    #already taken in getProductUrl
# print(new_product_link)

# new_response=requests.get(new_product_link,headers=HEADERS)

# # print(new_response)

# new_soup=BeautifulSoup(new_response.content,"html.parser")

# # We want Description , ASIN, Product Description and Manufacturer of the product

# desc=new_soup.find("div",attrs={"id":"productDescription"}).find("p").find("span").get_text()

# # print(desc)

# product_info=new_soup.find("ul",attrs={"class":"a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"}).find_all("li")
# # print(product_info);

# asin=product_info[3].text.strip()
# print(asin)

# manufacturer=product_info[7].text.strip()
# print(manufacturer)


import requests
from bs4 import BeautifulSoup
import pandas as pd


#  functions 



def getProductUrl(base_url):
    response=requests.get(base_url,headers=HEADERS)
    soup=BeautifulSoup(response.content,"html.parser")
    product_links=soup.find_all("a",attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    actual_link=product_links[0].get('href') 
    new_product_link="https://amazon.in" + actual_link 
    return new_product_link

def getProductName(soup):
    product_name=soup.find("span",attrs={"id":"productTitle" ,"class":"a-size-large product-title-word-break"}).get_text()
    return product_name


def getProductPrice(soup):
    product_price=soup.find("span",attrs={"class":"a-price-whole"}).get_text()
    return product_price

def getRating(soup):
    product_rating=soup.find("i",attrs={"class":"a-icon a-icon-star a-star-4 cm-cr-review-stars-spacing-big"}).find("span",attrs={"class":"a-icon-alt"}).get_text()
    return product_rating

def numberOfReviews(soup):
    all_product_review_link=soup.find("a",attrs={"data-hook":"see-all-reviews-link-foot","class":"a-link-emphasis a-text-bold"}).get("href")
    new_product_link = "https://amazon.in"+ all_product_review_link
    get_all_reviews_response=requests.get(new_product_link,headers=HEADERS)

    new_soup=BeautifulSoup(get_all_reviews_response,"html.parser")

    find_reviews_len=len(new_soup.find_all("div",attrs={"data-hook":"review","class":"a-section review aok-relative"}))

    return find_reviews_len


def getProductDescription(base_url):
    new_product_link=getProductUrl(base_url)
    new_response=requests.get(new_product_link,headers=HEADERS)
    new_soup=BeautifulSoup(new_response.content,"html.parser")
    desc=new_soup.find("div",attrs={"id":"productDescription"}).find("p").find("span").get_text()
    return desc


def getASIN(base_url):
    new_product_link=getProductUrl(base_url)
    new_response=requests.get(new_product_link,headers=HEADERS)
    new_soup=BeautifulSoup(new_response.content,"html.parser")
    product_info=new_soup.find("ul",attrs={"class":"a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"}).find_all("li")
    asin=product_info[3].text.strip()
    return asin



def getManufactureName(product_info):
   manufacturer_info=product_info[7].text.strip()
   return manufacturer_info

page_count=1

base_url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

HEADERS=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36','Accept-Language':'en-US, en;q=0.5'})

while page_count<=20:
    new_page_url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"+page_count
    new_product_url=getProductUrl(new_page_url)
    soup=BeautifulSoup(new_page_url.content,"html.parser")  # updated soup
    webpage=requests.get(new_page_url,HEADERS)  #new webpage link
    product_name=getProductName(soup)  # product name
    product_price=getProductPrice(soup) # product price
    product_rating=getRating(soup)  # product rating
    number_of_review=numberOfReviews(soup)  # no of review on the product
    product_desc=getProductDescription(new_page_url) # product desc
    asin=getASIN(new_page_url)  # get ASIN of the product
    new_soup=BeautifulSoup(webpage.content,"html.parser")
    product_info=new_soup.find("ul",attrs={"class":"a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"}).find_all("li")
    manufacture_name=getManufactureName(product_info)






