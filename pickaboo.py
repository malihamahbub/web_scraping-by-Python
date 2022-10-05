
import requests
from bs4 import BeautifulSoup
import json

def find_model_links(link_url="https://www.pickaboo.com/product/smartphone/"):
    
    source_code=requests.get(link_url)
    plain_text=source_code.text
    
    soup = BeautifulSoup(plain_text)

    products = soup.find('div',{'class':'product-listing-main col-sm-10'})
    prod_list = products.find('div',{'class':'row'})
    
    links = []
    for anc in prod_list.find_all('a'):
        anc_src = r'https://www.pickaboo.com' + anc.get('href')
        links.append(anc_src)
        
    return links

def extract_spec_from_link(link_url):
    
    source_code=requests.get(link_url)
    plain_text=source_code.text
    
    soup = BeautifulSoup(plain_text)
    
    results = []
    spec = soup.find('div',{'class':'more-information__grid'})
    for gvl in spec.find_all('div', {'detail-grid-view-line'}):
        for p in gvl.find_all('p'):
            results.append(p.getText())
    
    return results
            
def extract_from_pickaboo(link_url):
    
    source_code=requests.get(link_url)
    
    plain_text=source_code.text
    soup = BeautifulSoup(plain_text)

    results = []
    products = soup.find('div',{'class':'product-listing-main col-sm-10'})
    for anc in products.find_all('div', {'class':'product-one__single__inner__content'}):

        if anc.find('p', {'class':'product-price'}) is not None:
            results.append({
                'product': anc.find('p', {'class':'product-title'}).getText(),
                'price': anc.find('p', {'class':'product-price'}).getText()
            })

    specifications = {'configuration': results}
    json_object = json.dumps(specifications)

    with open("pickaboo_config.json", "w") as outfile:
        outfile.write(json_object)
    
    return specifications
            
if __name__ == "__main__":
    
    link_url="https://www.pickaboo.com/product/smartphone/"
    
    links = find_model_links(link_url)
    print("=====================================")
    print(links)
    specs = extract_spec_from_link(links[0])
    print("=================== Link 0 specs ==================")
    print(specs)
    print("================== all basic specs ===================")
    results = extract_from_pickaboo(link_url)
    print(results)
        







