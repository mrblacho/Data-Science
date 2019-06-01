import regex as re
from collections import Counter
from matplotlib import pyplot as plt
import csv
import requests
from bs4 import BeautifulSoup

web = 'https://ssearch.oreilly.com/?i=1;m_Sort=searchDate;q=data;q1=Books;x1=t1&act=pg_1' #since original link from book is no longer valid this is the recent one
soup = BeautifulSoup(requests.get(web).text, 'html5lib')  #souping the page

# here we create lists of data on individual books 
titles = []
years = []
authors = []

def get_titles(data): #get titles of books
    for title in data:
        titles.append(title.text.strip())

def get_date(dates):  #get year of issue
    for date in dates:
        years.append(date.text.split()[3])

def get_author(names):  #get author name
    for name in names:
        author = name.text
        if re.match('^By', author):
            authors.append(author)

base_url = 'https://ssearch.oreilly.com/?i=1;m_Sort=searchDate;page=' #beginning of url. We need to insert page number afterwards between base and end
end_url = ';q=data;q1=Books;x1=t1&act=pg_'
num_pages = 50  #the more history you want the more pages you need to check. This will also take more time to scrape.

for page_num in range(1, num_pages+1):  #here we scrape data from html, find titles, authors, years and append them into our lists
    print('souping page ', page_num, ' from ', num_pages)
    url = base_url + str(page_num) + end_url + str(page_num)  #we rebuild doccect url for each page
    soup = BeautifulSoup(requests.get(url).text, 'html5lib')
    f_title = soup.find_all('p', {'class': 'title'})  #find the book titles in the data
    f_date = soup.find_all('p', {'class': 'note date2'})  #find the book issue years in the data
    f_author = soup.find_all('p', {'class': 'note'})  #find the book authors in the data
    get_titles(f_title) #add titles found on page into list
    get_author(f_author)  #add authors found on page into list
    get_date(f_date)  #add years found on page into list

# this part is not necessary when you have too much time. In order to save time I saved the scraped data into simple text files
# if you scraped the data correctly you have them already available in text. In case you make mistake in further code you 
# don't need to scrape the pages again. Just get the data from texts and continue

with open('auth.txt', 'a') as f:
    for i in authors:
        f.write(i + '\n')

with open('titles.txt', 'a') as f:
    for i in titles:
        f.write(i + '\n')

with open('years.txt', 'a') as f:
    for i in years:
        f.write(i + '\n')

data = [] #add content of years into this list
with open('years.txt') as f:
    for line in f:
        data.append(line.strip()) #add each year into list

sorted_data = Counter(data) #calculate how many books were issued each year (simply count all the occurence of year in the list)

plt.gca().invert_xaxis() #plot came with inverted x-axis, which looked weird. This makes it correct. 
plt.plot(sorted_data.keys(), sorted_data.values())  #plot of number of books per year
