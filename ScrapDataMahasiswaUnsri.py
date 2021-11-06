import requests
import csv
from bs4 import BeautifulSoup
import re
import timeit
import urllib.request


start = timeit.default_timer()


def writetoCSV(file, data):
    with open(f'Hasil_Scrap_Mahasiswa_Unsri/{file}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([file])
        writer.writerow(header)
        writer.writerows(data)


path_link_scrap = "Url/LinkMahasiswaUnsri-temp.csv"
with open(path_link_scrap, 'r') as file:
    jurusan = file.readlines()


header = ["NIM", "NAMA", "FAKULTAS / PRODI",
          "JENIS KELAMIN", "AGAMA", "ASAL SMA", "STATUS"]


for i in jurusan:
    i = i.strip()
    path = "http://old.unsri.ac.id/"+i
    page = requests.get(path, proxies=urllib.request.getproxies())
    after_bs = BeautifulSoup(page.content, 'html.parser')
    find_data = after_bs.find_all('a')

    # hanya ambil link yg awalnya ?act=detil_krs_mahasiswa&mhs
    temp = "?act=detil_krs_mahasiswa&mhs"
    listLink = []
    for j in find_data:
        j = j.get("href")
        if temp in j:
            listLink.append(j)

    dataMahasiswa = []
    for k in listLink:
        path = "http://old.unsri.ac.id/"+k
        page = requests.get(path, proxies=urllib.request.getproxies())
        after_bs = BeautifulSoup(page.content, 'html.parser')

        temp = []
        for item in header:
            if item == "NIM":
                find = after_bs.find("th", text=item).findNext("td")
                find = find.get_text(strip=True)
                find = f'"{find}"'
                temp.append(find)
            else:
                find = after_bs.find("th", text=item).findNext("td")
                temp.append(find.get_text(strip=True))

        dataMahasiswa.append(temp)

    hasil = re.findall("fak_prodi=([0-9-]+).+angkatan=([0-9]+)", i)
    file = f"prodi {hasil[0][0]} angkatan {hasil[0][1]}"

    writetoCSV(file, dataMahasiswa)


stop = timeit.default_timer()

print('Success\nTime: ', stop - start)
