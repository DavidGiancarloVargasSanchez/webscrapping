from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

""" Creating the functions """
# 1. Function to obtain all the products in a single page (in this case, cars are the products)
def get_products(url):
    # Obtain a response of the base_url (sendind an http request)
    page = requests.get(url)

    # Verify if the response is successfull 
    if page.status_code == requests.codes.ok:
        # get the whole page
        bs = BeautifulSoup(page.text, 'lxml')

    # Obtains the main container
    main_container = bs.find('div', class_='content')

    # Obtains the container that holds the products
    products_container = main_container.find('ul', class_='rows')

    # Obtain all the products
    all_products = products_container.find_all('li', class_='result-row')

    return title_price(all_products)

# 2. Function to save the product's title and price into the dictionary
def title_price(products):    
    # for product in all_products:
    for product in products:
        title = product.find('a', class_='result-title hdrlnk').text
        if title:
            data['Title'].append(title)
        else:
            data['Title'].append('N/A')

        price = product.find('span', class_='result-price').text
        if price:
            data['Price'].append(price)
        else:
            data['Price'].append('N/A')
    
    return data['Title'], data['Price']

# 3. Function to go to the next page
def next_page(url, following_page):
    base_new = ''
    for u in url:
        if u == '&':
            break
        else:
            base_new += u
    amp_position = url.find('&')
    rest_url = url[amp_position:]
    
    new_url = base_new + '=&s=' + str(following_page) + rest_url
    
    return get_products(new_url)


""" Logic of the program """
# Assign webpage to be scraped to our variable
base_url = 'https://honolulu.craigslist.org/search/sss?query=cars&sort=rel'

# Create a dictionary to store the products (cars)
data = {
    'Title': [],
    'Price': []
}

# Obtain the products of the first page
get_products(base_url)

# Finding the total items (cars) of all the pages
page = requests.get(base_url)
bs = BeautifulSoup(page.text, 'lxml')
total_pages_items = int(bs.find('span', class_='totalcount').text)

# Logic to run all pages
next_page_beginning  = 120
while next_page_beginning <= total_pages_items:
    next_page(base_url, next_page_beginning)
    next_page_beginning += 120
    

""" Using pandas """
# 1. Creating the dataframe with its columns
df = pd.DataFrame(data, columns=['Title','Price'])

# 2. Replacing the '$' and ',' in order to ordering the dataframe 
df['Price'] = df['Price'].str.replace(',','').str.replace('$','').astype('float')

# 3. Ordering the dataframe in descending order by price (highest to lowest)
df = df.sort_values(by=['Price'], ascending=False)

# 3. Making the index starsts in 1
df.index = df.index + 1

# 4. Creating the csv file
df.to_csv('craigslist_cars_file.csv', sep=',', index=False, encoding='utf-8')


print('Done')
