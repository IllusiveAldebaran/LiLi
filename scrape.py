#!/usr/bin/python3.12
# TODO: make the scraping a function because it runs once and then enters a function, when it could just be calling the same function. Redundant.

from bs4 import BeautifulSoup # xml (html) parser, way better than ElementTree
from urllib.request import urlopen

# for writing output files
#import os 
import csv

thread_id=45708# or 42680 
thread_url="https://www.mafiauniverse.com/forums/threads/{}/page".format(thread_id)


page_num = 1;
post_usernames = list()
post_dates = list()
post_content = list()

# get first page info
url = thread_url + str(page_num)
html = urlopen(url).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
thread_title = soup.find("span", class_="bbc_title").text
# Gives all the html spit out
# print(soup)

print("Scraping pages: ", end="")
# As long as there is more pages, keep scraping
while(url != None):
    print("{} ".format(page_num),end="", flush=True)
    # posts on a page
    posts = soup.find("ol", id="posts").find_all("li", recursive=False)

    
    # Might be useful later?
    #posts_ids = [tag.get('id') for tag in posts]
    
    # what she wanted
    post_usernames += [tag.find("div", class_="postdetails").find("a", class_="username").text for tag in posts]
    post_dates += [tag.find("div", class_="posthead").find("span", class_="date").text for tag in posts]
    post_content += [tag.find("div", class_="postdetails").find("div", class_="content") for tag in posts]
    
    url = soup.find("a" , rel="next");
    if(url != None):
        page_num += 1;
        url = thread_url + str(page_num)
        html = urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
    # INFO: A lot of these links have blocks of previous posts, so exclude the div of class "bbcode_container" to exclude responses and get original content
print() # new line
print("Scraping thread {}".format(thread_title))


print("Putting posts in \"{}-posts\".csv".format(thread_title))
spamWriter = csv.writer(open(thread_title+"-posts.csv", 'w'))

# Convert the modified XML tree to string
output = soup.prettify()
#print(modified_xml) # debug

spamWriter.writerow(["Date","Username", "Content"])
for i in range(len(post_dates)):
    spamWriter.writerow([post_dates[i], post_usernames[i], post_content[i]])

 
# For debugging and reading out of the csv (making sure what we're scraping is parsable by some method)
file = open("{}-posts.csv".format(thread_title))
csvreader = csv.reader(file)
rows = list()
for row in csvreader:
    rows.append(row)
