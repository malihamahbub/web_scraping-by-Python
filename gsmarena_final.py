import requests
from bs4 import BeautifulSoup
import json


def find_brand_link(link_url="http://www.gsmarena.com/"):
    c = 1
    source_code=requests.get(link_url)
    plain_text=source_code.text
    soup = BeautifulSoup(plain_text)
    
    results = {}
    
    for link in soup.find_all('div',{'class':'brandmenu-v2 light l-box clearfix'}):
        for li in link.find_all('li'):
            for anc in li.find_all('a'):
                anc_src = r'http://www.gsmarena.com/' + anc.get('href')
                anc_name = anc.string
                results[anc_name] = anc_src
                
    return results

def find_model_link(hrefs):
    
    results = []
    
    i = 1
    source_code=requests.get(hrefs)
    plain_text=source_code.text
    soup = BeautifulSoup(plain_text)
    for link in soup.find_all('div',{'class':'makers'}):
        for li in link.find_all('li'):
            for anc in li.find_all('a'):
                anc_src = r'http://www.gsmarena.com/' + anc.get('href')
                for nam in (sp.find('span') for sp in anc.find_all('strong')):
                    model_name = nam.string
                    results.append((anc_src, model_name))
    return results              

def find_specifications(m_link):

    source_code = requests.get(m_link)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    
    specifications = {}
    
    specs_list = soup.find('div', {'id':'specs-list'})
    
    return specs_list

def format_and_save_results(specs_list):
    
    results =[]
    for table in specs_list.find_all('table'):

        table_data = [[cell.text for cell in row("td")]
                             for row in table.find_all("tr")]
        results.append(dict(table_data))

    specifications = {'configuration': results}
    json_object = json.dumps(specifications)

    with open("gsmarena_config.json", "w") as outfile:
        outfile.write(json_object)

    print(specifications)