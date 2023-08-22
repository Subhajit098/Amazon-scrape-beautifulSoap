
import requests
from bs4 import BeautifulSoup
import pandas as pd


#  functions 



def getProductUrl(base_url,ind):
    response=requests.get(base_url,headers=HEADERS)
    soup=BeautifulSoup(response.content,"html.parser")
    product_links=soup.find_all("a",attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    actual_link=product_links[ind].get('href') 
    new_product_link="https://amazon.in" + actual_link 
    return new_product_link

def getProductName(soup):
    try:
      product_name=soup.find("span",attrs={"id":"productTitle" ,"class":"a-size-large product-title-word-break"})

      title=product_name.text

      title_string=title.strip()

    except AttributeError:
        title_string=""

    return title_string


def getProductPrice(soup):
    try:
        product_price=soup.find("span",attrs={"class":"a-price-whole"}).string.strip()
    except AttributeError:
        product_price=""    
    return product_price

def getRating(soup):
    try:
      product_rating=soup.find("i",attrs={"class":"a-icon a-icon-star a-star-4 cm-cr-review-stars-spacing-big"}).find("span",attrs={"class":"a-icon-alt"}).string.strip()
    except AttributeError:
        product_rating=""

    return product_rating

def numberOfReviews(soup):

  try:
    all_product_review_link=soup.find_all("a",attrs={"data-hook":"see-all-reviews-link-foot","class":"a-link-emphasis a-text-bold"}).get("href")
    new_product_link = "https://amazon.in"+ all_product_review_link
    get_all_reviews_response=requests.get(new_product_link,headers=HEADERS)

    try:
        new_soup=BeautifulSoup(get_all_reviews_response,"html.parser")

        find_reviews_len=len(new_soup.find_all("div",attrs={"data-hook":"review","class":"a-section review aok-relative"}))

    except AttributeError:
        find_reviews_len=0
  except AttributeError:    
    find_reviews_len=0

  return find_reviews_len


def getProductDescription(soup):
    try:
       desc=soup.find("div",attrs={"id":"productDescription"}).find("p").find("span").get_text()
    except AttributeError:
       desc=""   
       
    return desc


def getASIN(soup):
    try:
       product_info=soup.find("ul",attrs={"class":"a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"}).find_all("li")
       asin=product_info[3].text.strip()

    except AttributeError:
          asin=""
    return asin



def getManufactureName(soup):
   product_info=soup.find("ul",attrs={"class":"a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"}).find_all("li")[7].find("span")
   manufacturer_info=product_info.text.strip()
   return manufacturer_info




if __name__=='__main__':
   
   page_count="1"
   
   base_url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

   HEADERS=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36','Accept-Language':'en-US, en;q=0.5'})

   new_page_url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"+page_count

   webpage=requests.get(new_page_url,headers=HEADERS)

   soup=BeautifulSoup(webpage.content,"html.parser")

   links=soup.find_all("a",attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

   links_array=[]
   for link in links:
      links_array.append(link.get("href"))

   d={"Description":[],"ASIN":[],"Manufacturer":[]}   

   for link in links_array:
      new_webpage = requests.get("https://www.amazon.in"+link,headers=HEADERS)

      new_soup=BeautifulSoup(new_webpage.content,"html.parser")

      d['ASIN'].append(getASIN(new_soup))
      
      d["Manufacturer"].append(getManufactureName(new_soup))

      d["Description"].append(getProductDescription(new_soup))


   amazon_data_sheet = pd.DataFrame.from_dict(d)  
   amazon_data_sheet.to_csv("./data/amazon_data.csv",header=True,index=False) 
   





