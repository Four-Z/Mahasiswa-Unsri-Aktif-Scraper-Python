import requests
import csv
from bs4 import BeautifulSoup
import re
import timeit
import urllib.request

start = timeit.default_timer()

def writetoCSV(file, data):
    with open(f'temp/{file}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # writer.writerow([file])
        # writer.writerow(header)
        writer.writerows(data)


path_link_scrap = "Url/LinkFakultasILKOM.txt"
with open(path_link_scrap, 'r') as file:
    jurusan = file.readlines()


header = ["NIM", "NAMA", "FAKULTAS / PRODI",
          "JENIS KELAMIN", "AGAMA", "ASAL SMA", "STATUS"]

count = 0
session = requests.Session()
for i in jurusan[:1]:
    i = i.strip()
    # path = "http://old.unsri.ac.id/"+i
    path = i
    page = session.get(path, proxies=urllib.request.getproxies(), verify=False)
    after_bs = BeautifulSoup(page.content, 'html.parser')
    find_data = after_bs.find_all('a')

    # hanya ambil link yg awalnya ?act=detil_krs_mahasiswa&mhs
    temp = "?act=detil_mahasiswa&mhs"
    listLink = []
    for j in find_data:
        j = j.get("href")
        if temp in j:
            listLink.append(j)

    # remove duplicate link
    listLink = list(dict.fromkeys(listLink))

    #scrap data
    dataMahasiswa = []
    for k in listLink:
        path = "http://old.unsri.ac.id/"+k
        page = session.get(path, verify=False)
        after_bs = BeautifulSoup(page.content, 'html.parser')

        temp = []
        for item in header:
            if "FAKULTAS" in item:
                find = after_bs.find("th", text=item).findNext("td")
                find = find.get_text(strip=True)
                # split between fakultas and prodi
                find = find.split(" / ")
                temp.append(find[0])
                temp.append(find[1])
            elif "ANGKATAN" in item:
                angkatan = k[len(k)-1:len(k)-5]
                temp.append(angkatan)
            else:
                find = after_bs.find("th", text=item).findNext("td")
                find = find.get_text(strip=True)
                temp.append(find)

        dataMahasiswa.append(temp)

    hasil = re.findall("fak_prodi=([0-9-]+).+angkatan=([0-9]+)", i)
    file = f"prodi {hasil[0][0]} angkatan {hasil[0][1]}"

    writetoCSV(file, dataMahasiswa)
    print(count)
    count += 1

stop = timeit.default_timer()
print('Success\nTime: ', stop - start)
