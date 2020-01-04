import requests
from bs4 import BeautifulSoup
import os
all_links=[]
def sublinks(url):
    with requests.session() as r:
        response=r.get(url)
        html=response.content
        soup=BeautifulSoup(html,features='html.parser')
        counter=0
        subs=[]
        while(1):
            counter+=1
            if(soup.find_all('div',{'class':f'unitbox unit{counter}'})==[]):
                break
            list=soup.select(f'div.unitbox.unit{counter} a')
            for i in range(len(list)):
                subs.append("https://btech.rgpvnotes.in"+list[i].get('href'))
        return subs

def getContent(url):
    with requests.session() as r:
        response = r.get(url)
        html = response.content
        soup = BeautifulSoup(html, features='html.parser')
        ModuleName=""
        for name in soup.find_all('h5',{'class':'tc-title tc-title-center'}):
            ModuleName=name.text.strip()
        ModuleName=ModuleName.replace('/', '|')
        print("Creating Directory for "+str(ModuleName))


        path="/media/dayhawk/New HDD/Archive/"+str(ModuleName)
        if(os.path.exists(path)):
            print("Directory Already Exists")
        else:
            os.mkdir(path)
        coun=0
        download_links = ""
        for download in soup.find_all('a',{'rel':'external nofollow noreferrer'}):
            coun+=1
            download_links+=download.get('href').strip()+"\n"
            if(coun%2==0):
                down_path=path+"/Unit"+str(coun/2)
                if(os.path.exists(down_path)):
                    print("Content Already Exists")
                else:
                    os.mkdir(down_path)
                    unit=open(down_path+"/"+str(coun/2)+".txt",'w')
                    unit.write(download_links)
                    unit.flush()
                download_links=""



homelinks=open("./Sources/rgpvnotes","r")
homelinkslist=homelinks.readlines()
for home in homelinkslist:
    for links in sublinks(home.strip()):
        if(links=="https://btech.rgpvnotes.in"):
            continue
        all_links.append(links)
for link in all_links:
    getContent(link)