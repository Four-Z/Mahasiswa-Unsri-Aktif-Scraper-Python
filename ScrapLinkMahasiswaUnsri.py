import requests
import csv
from bs4 import BeautifulSoup


path_scrap = "http://old.unsri.ac.id/?act=daftar_mahasiswa"
page = requests.get(path_scrap)

after_bs = BeautifulSoup(page.content, 'html.parser')
find_data = after_bs.find_all('a')

temp = "?act=daftar_mahasiswa&fak_prodi="

path_write_link = 'Url/LinkMahasiswaUnsri.txt'
f = open(path_write_link, 'w')
for i in find_data:
    i = i.get("href")
    if temp in i:
       f.write("http://old.unsri.ac.id/"+i)
       f.write('\n')
            
                
                



