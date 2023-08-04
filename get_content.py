import requests
from bs4 import BeautifulSoup
from typing import List


def scrape_text_to_file(url: str, filename: str) -> str:
    """
    Scrape the text of a webpage into a text file. 
    Only get the text contained in a div with id="block-bsi-content".

    Parameters:
    url (str): The URL of the webpage to scrape.
    filename (str): The name of the file to write the text to.
    """

    # Send a GET request to the webpage
    response = requests.get(url)

    # Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div with id="block-bsi-content" and get its text
    text = soup.find('div', id='block-bsi-content').get_text()

    while '\n\n' in text:
        text = text.replace('\n\n','\n')

    # Write the text to the file
    with open(filename, 'w') as f:
        f.write(text)
    
    return text


def scrape_urls(url: str, string: str, exclude:List=None, level:str='one') -> List[str]:
    """
    Fetch a webpage and extract all URLs that contain a specific string.

    Args:
        url (str): The URL of the webpage to scrape.
        string (str): The string to look for in the URLs.
        exclude (List[str]): A list of strings to exclude from the URLs.

    Returns:
        List[str]: A list of URLs from the webpage that contain the string.
    """

    # Send a GET request to the webpage
    response = requests.get(url)

    # Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    urls = []

    # Find all 'a' tags with href attribute on the webpage
    for a in soup.find_all('a', href=True):

        # If the string is found in the href of the 'a' tag,
        # append it to the urls list
        if string in a['href']:
            urls.append(a['href'])

    # Remove duplicate URLs
    urls = list(set(urls))


    remove_urls = []

    # Remove URLs that contain the exclude strings
    for url in urls:
        for exlude_str in exclude:
            if exlude_str in url.lower():
                remove_urls.append(url)
        # Remove the URL if it is the same as the string
        if url == string:
            remove_urls.append(url)
        # Remove the URL if it for a content node if we're traversing the homepage
        if level == 'one':
            if url.count('/') > 3:
                remove_urls.append(url)
        # Remove the URL if it for a category node if we're traversing the category page
        elif level == 'two':
            if url.count('/') == 3:
                remove_urls.append(url)
    return [url for url in urls if url not in remove_urls]


# first set up some variables
homepage_stem = 'https://www.immunology.org'
homepage_url = f"{homepage_stem}/bitesized-immunology"
string = '/public-information/bitesized-immunology'
exclude = ['login','site-map']
content_folder = 'content'

content_urls = []

# scrape the homepage for urls
urls = scrape_urls(homepage_url, string, exclude=exclude)

# iterate through the urls on the homepage
for url in urls:
    # scrape the category page for urls
    category_page_url = f"{homepage_stem}{url}"
    urls = scrape_urls(category_page_url, string, exclude=exclude, level='two')
    # output the number of urls found on the category page
    print (f"Number of urls found on {category_page_url}: {len(urls)}")
    # iterate through the urls on the category page and only store unique urls
    for url in urls:
        if url not in content_urls:
            content_urls.append(url)


print (f"Total number of content page urls found :{len(content_urls)}")

filenames = {}

# iterate through the content page urls and scrape the text to a file
for url in content_urls:
    # create a filename from the url
    filename = f"{content_folder}/{url.replace('/public-information/bitesized-immunology/','').replace('/','-')}.txt"
    
    content_page_url = f"{homepage_stem}{url}"

    # add the filename to the filenames dict, which maps to the url
    filenames[filename] = content_page_url
    print (f"Scraping {content_page_url} to {filename}")

    text = scrape_text_to_file(content_page_url, filename)

    print (f"Length of text scraped = {len(text)}")