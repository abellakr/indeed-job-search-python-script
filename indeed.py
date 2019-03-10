import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd
import time

def URLGen(country, job, location, salary):
    URLJob = "+".join(job.split())
    URLLoc = "+".join(location.split())
    sal = float(salary)/1000
    URLSal = "24"+str(sal)

    if country == 'US':
        URL = "https://www.indeed.com/jobs?q="+str(URLJob)+"+24"+str(URLSal)+"%2C000&l="+str(URLLoc)
    elif country == 'CA':
        URL = "https://ca.indeed.com/jobs?q="+str(URLJob)+"+24"+str(URLSal)+"%2C000&l="+str(URLLoc)
    else:
        print("thats not a valid option.")
        URL = ''

    return(URL)

def extract_job_title_from_result(soup):
    jobs = []
    for div in soup.find_all(name="div",attrs={"class":"row"}):
        for a in div.find_all(name="a",attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return(jobs)

def extract_location_from_result(soup):
    locations = []
    spans = soup.find_all("span", attrs={"class": "location"})
    for span in spans:
        locations.append(span.text)
    return(locations)

def extract_salary_from_result(soup):
    salaries = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        try:
            salaries.append(div.find("nobr").text)
        except:
            try:
                div_two = div.find(name="div", attrs={"class":"sjcl"})
                div_three = div_two.find("div")
                salaries.append(div_three.strip())
            except:
                salaries.append("Nothing found")
    return(salaries)

def extract_summary_from_result(soup):
    summaries = []
    spans = soup.find_all("span", attrs={"class":"summary"})
    for span in spans:
        summaries.append(span.text.strip())
    return(summaries)

def findJobs(URL):
    if URL != '':
        #conducting a request of the stated URL above:
        # print(URL)
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, "html.parser")
        # print(soup.prettify())
            
        jobs = extract_job_title_from_result(soup)
        locations = extract_location_from_result(soup)
        salaries = extract_salary_from_result(soup)
        # sumamries = extract_summary_from_result(soup)

        fmt = '%-10s%-60s%-70s%s'
        # print(fmt % ('', 'Job title', 'Location', 'salary'))
        for i, (job, location, salary) in enumerate(zip(jobs, locations, salaries)):
            print(fmt % (i, job, location, salary))

def PageGen(URL):
    pageUrls = []
    for x in range(10, 40, 10):
        pageUrls.append(URL+"&start="+str(x))
    return pageUrls

# inputs
country = input("which country are looking to work in (CA/US)?: ")
job = input("type of job you're looking for: ")
location = input("desired location: ")
salary = input("desired salary: ")

# grab URL
URL = URLGen(country, job, location, salary)

#grab page Urls
pageUrls = PageGen(URL)

x = 1
# find jobs
fmt = '%-10s%-60s%-70s%s'
print(fmt % ('', 'Job title', 'Location', 'salary'))
for page in pageUrls:
    print("Page "+str(x))
    findJobs(page)
    x = x + 1




