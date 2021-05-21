import re
import pandas as pd

from bs4 import BeautifulSoup
from urllib.request import urlopen

CLEAN = re.compile('<.*?>')

def open_and_returns_bs4_object(url):
    html = urlopen(url)
    return BeautifulSoup(html)


if __name__ == '__main__':
    with open("webportos.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

        porto, complemento = [], []

        for ahref in soup.find('ul', {'id': 'listaPortos'}).find_all('a'):
            obj = open_and_returns_bs4_object(ahref['href'])
            ps = obj.find('div', {'class': 'informacoes'}).find_all('p')

            test = ''
            for p in ps:
                test += re.sub(CLEAN, '', str(p).strip())

            porto.append(obj.find('div', {'class': 'titles'}).find('h1').text)
            complemento.append(test)
        
        writer = pd.ExcelWriter('portos.xlsx', engine='xlsxwriter')
        df = pd.DataFrame(
            {'Porto': porto, 'Complemento': complemento}
        )
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
