import requests
from bs4 import BeautifulSoup
import re
import urllib
from urllib.parse import urljoin
import argparse


address = 'https://www.cs.ccu.edu.tw/'
linklist = list()               #store all links
done = list()                   #
flag = 0                    #index of linklist


def findlinks(address):
    links = set()
    try :
        if not address.endswith('flv') and not address.endswith('pdf') and not address.endswith('mp4') and not address.endswith('jpg'):
            url = requests.get(address) 
            soup = BeautifulSoup(url.content,'html.parser')

            while(address.rfind('/') > 8):   #normalize web addr
                rnum=address.rfind('/')
            # print(rnum)
                address = address[0:rnum]
    
            nor_url = address + '/'
            # print(nor_url)

            for data in soup.findAll('a',href = True ):         
                if data['href'][0:4] == 'http' :             #process the redirection            
                    links.add(data['href'])      
                
                else : 
                    if data['href'][0:4] != 'mail' and data['href'][0:4] != 'tcp':
                        data['href'] = urljoin(nor_url,data['href'])
                        links.add(data['href'])
                    else: 
                        pass

            for link in links:
                if link not in done:
                    linklist.append(link)
                # print(link)
        else:
            pass
    except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) : 
        pass


def findemails(links):
    try : 
        if not links.endswith('flv') and not links.endswith('pdf') and not links.endswith('mp4') and not links.endswith('jpg'):
            if links[0:4] == 'http' :
            
                link = requests.get(links)

                result = set()
                allemails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",link.text,re.I)
                print(links,' : ')
                # print(emails)

                for email in allemails:
                    result.add(email)
                print()
                for single in result:
                    print(single)
                print()
            else:
                pass
        else : 
            pass

    except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) : 
        pass




def link_to_email(address):   # the href in this page's emails //hyperlink's email
    # findemails(address)    
    links = findlinks(address)
    for link in links:
        findemails(link)

def crawl(address): 
    linklist.append(address)

    # print(linklist[0])
    while linklist:
        link = linklist.pop(0)
        # print(link)
        done.append(link)
        findemails(link)                
        findlinks(link)



        
if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('address',help="Input your web site.",type=str)        
    args = parse.parse_args()
    if args.address[0:4] != 'http':
        args.address = 'http://' + args.address
    function = crawl(args.address)
    function()

# threading.Thread(target = recursive,args = (address,)).start()
# threading.Thread(target = printe,args = ()).start()











