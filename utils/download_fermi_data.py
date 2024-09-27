#%%
import numpy as np
import requests
import time
from tqdm.contrib.concurrent import process_map
import os
import argparse

CBLUE = '\033[34m'
CEND = '\033[0m'



#%%
def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(CBLUE + box + CEND)

def download_url(args):
    t0 = time.time()
    url, fn = args[0], args[1]
    if os.path.exists(fn):
        # the file already exists, skipping
        return (url, time.time() - t0)
    else:
        try:
            r = requests.get(url)
            with open(fn, 'wb') as f:
                f.write(r.content)
            # print('url:', url, 'time (s):', time.time() - t0)
            return (url, time.time() - t0)
        except Exception as e:
            print('Exception in download_url():', e)



def download_parallel(iter, total, num_workers=None):
    if num_workers is None:
        num_workers = os.cpu_count()-1
    if total > num_workers*100:
        chuncksize = np.min([1, int(np.floor(total/(num_workers*100)))]) 
    else:
        chuncksize=1

    res = process_map(download_url, iter,
                      max_workers=num_workers, chunksize=chuncksize, total=total)
    return res
#%%
class fermi_data_dowloader:
    def __init__(self, week_in, week_out, root):

        self.week_in = week_in
        self.week_out = week_out
        self.gll_psc_v = 35
        self.num_workers=None
        self.base_path=root

        self.download_photon_data_flag=True
        self.download_spacecraft_data_flag=False
        self.download_4FGL_catalogue_flag=True

        
        return
    
    def download_photon_data(self):
        download_folder = f"{self.base_path}/photon"
        os.makedirs(download_folder, exist_ok=True)

        urls = []
        destinations = []
        for i in np.arange(self.week_in , self.week_out+1):
            urls.append(f"https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/lat_photon_weekly_w{i:03d}_p305_v001.fits")
            destinations.append(f"{download_folder}/lat_photon_weekly_w{i:03d}_p305_v001.fits")

        idx = np.random.permutation(len(urls))
        inputs = zip(np.array(urls)[idx], np.array(destinations)[idx])

        #%%

        print_msg_box("Downloading photon data")
        download_parallel(inputs, len(urls), num_workers=self.num_workers)
        print("done")
        return
    
    def download_spacecraft_data(self):
        download_folder = f"{self.base_path}/spacecraft"
        os.makedirs(download_folder, exist_ok=True)

        url = "https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/mission/spacecraft/lat_spacecraft_merged.fits"
        destination = f"{download_folder}/lat_spacecraft_merged.fits"

        inputs = (url, destination)

        print_msg_box("Downloading spacecraft file")
        download_url(inputs)
        print("done")
        return
    
    def download_4FGL_catalogue(self):
        download_folder = f"{self.base_path}/4FGL"
        os.makedirs(download_folder, exist_ok=True)
        url = f"https://fermi.gsfc.nasa.gov/ssc/data/access/lat/14yr_catalog/gll_psc_v{self.gll_psc_v}.fit"
        destination = f"{download_folder}/gll_psc_v{self.gll_psc_v}.fit"
        inputs = (url, destination)

        print_msg_box("Downloading 4FGL catalogue")
        download_url(inputs)
        print("done")
        return
    
    def download_all(self):
        if self.download_photon_data_flag:
            self.download_photon_data()

        if self.download_spacecraft_data_flag:
            self.download_spacecraft_data()

        if self.download_4FGL_catalogue_flag:
            self.download_4FGL_catalogue()
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root", type=str)
    parser.add_argument("--week_in", type=int, default=9)
    parser.add_argument("--week_out", type=int, default=795)
    args = parser.parse_args()

    root=args.root
    week_min=args.week_in
    week_max=args.week_out

    downloader=fermi_data_dowloader(week_min, week_max, root)
    downloader.download_all()

    

