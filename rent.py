import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

houselist = []
#Function 
def get_houses(page):
    url = 'https://www.buyrentkenya.com/flats-apartments-for-rent?page='+str(page)

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    rentals=soup.find_all('div', class_='mb-3 w-full')
    
    for item in rentals:
        try:
            bedrooms = item.find('span', {'data-cy':'card-beds'}).text.replace('\n','')
        except:
            bedrooms = None
        try:
            bathrooms = item.find('span', {'data-cy':'card-beds'}).text.replace('\n','')
        except:
            bathrooms = None
        try:
            owner = item.houses.find('p', class_='text-base').text
        except:
            owner = 'Not listed'
        try:
            listed_on = item.find('span', class_='text-white text-xs text-right leading-4').text.replace('Added','')
        except:
            listed_on = None

        house = {
           
        'location':item.find('p', class_='text-md md:text-sm font-normal text-grey-darker mt-1 md:mt-0').text.replace('\n',''),
        'rent': item.find('a',class_='no-underline').text.replace('\n','').replace('KSh ',''),
        
        'bedrooms': bedrooms,
        'bathrooms':bathrooms,


        'Description': item.find('a', class_='no-underline text-black').text.replace('\n',''),
        #'owner': owner,
        'listed_on': listed_on

        
        
        
        }
        houselist.append(house)
    return
#call the function using for loop with number of pages to crawl 
for x in range(1,160):
    get_houses(x)
    

df = pd.DataFrame(houselist)
df.to_excel('hous_list.xlsx', index=False)

print(len(houselist))