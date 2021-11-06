import requests
import csv
from bs4 import BeautifulSoup

path_scrap = "http://old.unsri.ac.id/?act=daftar_mahasiswa"
page = requests.get(path_scrap)

after_bs = BeautifulSoup(page.content, 'html.parser')
find_data = after_bs.find_all('a')

temp = "?act=daftar_mahasiswa&fak_prodi="
tahun = ["2016", "2017", "2018", "2019", "2020", "2021"]
clearLink = []
# hanya ambil link yg awalnya ?act=daftar_mahasiswa&fak_prodi= dan tahun >=2016
for i in find_data:
    i = i.get("href")
    if temp in i:
        for th in tahun:
            if th in i:
                clearLink.append(i)

path_write_link = 'Url/LinkMahasiswaUnsri.csv'
with open(path_write_link, 'w', newline='') as f:
    writer = csv.writer(f)
    for i in clearLink:
        writer.writerow([i])
