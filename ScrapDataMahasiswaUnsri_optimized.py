import requests
import csv
from bs4 import BeautifulSoup
import re
import timeit
from tqdm import tqdm
import time
import urllib.request
import concurrent.futures
import logging
import http.client



# activating logging to help uncover what goes wrong
# http.client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


def writetoCSV(file, data):
    with open(f'temp/{file}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def get_mahasiswa_link(i, session):
    # request each link in https://old.unsri.ac.id/?act=daftar_mahasiswa

    # with proxy
    page = session.get(i.strip(), proxies=urllib.request.getproxies(), verify=False)

    # without proxy
    # page = requests.get(i.strip(), verify=False)

    # find all tag <a> using bs4
    after_bs = BeautifulSoup(page.content, 'html.parser')
    find_data = after_bs.find_all('a')

    # only get link start with '?act=detil_krs_mahasiswa&mhs'
    temp = "?act=detil_mahasiswa&mhs"
    linkMahasiswa = []
    for j in find_data:
        j = j.get("href")
        if temp in j:
            linkMahasiswa.append("http://old.unsri.ac.id/"+j)

    # remove duplicate link
    linkMahasiswa = list(dict.fromkeys(linkMahasiswa))
    return linkMahasiswa



def scrapMahasiswa(i):
    header = ["NIM", "NAMA", "FAKULTAS / PRODI",
            "JENIS KELAMIN", "AGAMA", "ASAL SMA", "STATUS"]

    # This makes sure the connection to the server stays open
    session = requests.Session()

    linkMahasiswa = get_mahasiswa_link(i, session)
    #scrap each data mahasiswa in linkMahasiswa
    dataMahasiswa = []
    for k in linkMahasiswa:
        # with proxy
        page = session.get(k.strip(), proxies=urllib.request.getproxies(), verify=False)

        # without proxy
        page = session.get(k.strip(), verify=False)
        after_bs = BeautifulSoup(page.content, 'html.parser')

        data = []
        for item in header:
            if "FAKULTAS" in item:
                find = after_bs.find("th", text=item).findNext("td")
                find = find.get_text(strip=True)

                # split between fakultas and prodi
                find = find.split(" / ")
                data.append(find[0])
                data.append(find[1])
            # elif "ANGKATAN" in item:
            #     angkatan = k[len(k)-1:len(k)-5]
            #     data.append(angkatan)
            elif "NIM" in item:
                find = after_bs.find("th", text=item).findNext("td")
                find = find.get_text(strip=True)

                # add "" in NIM
                find = '"'+find+'"'
                data.append(find)
            else:
                find = after_bs.find("th", text=item).findNext("td")
                find = find.get_text(strip=True)
                data.append(find)

        dataMahasiswa.append(data)

    #generate file name using regex
    generateFilename = re.findall("fak_prodi=([0-9-]+).+angkatan=([0-9]+)", i)
    # set filename
    filename = f"prodi_{generateFilename[0][0]}_angkatan_{generateFilename[0][1]}"

    # save to csv format for each angkatan
    writetoCSV(filename, dataMahasiswa)
    

def doScarp(daftarMahasiswa):
    # daftarMahasiswa = daftarMahasiswa[:1]

    #depends on your computer specs
    MAX_THREADS = 30
    threads = min(MAX_THREADS, len(daftarMahasiswa))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        result = list(tqdm(executor.map(scrapMahasiswa, daftarMahasiswa), total = len(daftarMahasiswa)))
    
    return result

def main():
    # link daftar mahasiswa from ScapLinkMahasiswaUnsri.py
    # path_link_scrap = "Url/LinkMahasiswaUnsri.txt"
    path_link_scrap = "Url/LinkFakultasKedokteran.txt"
    with open(path_link_scrap, 'r') as file:
        daftarMahasiswa = file.readlines()

    start = timeit.default_timer()
    doScarp(daftarMahasiswa)

    # time to know how long scrap needed
    stop = timeit.default_timer()
    print('Success\nTime: ', stop - start)

# start program
main()


