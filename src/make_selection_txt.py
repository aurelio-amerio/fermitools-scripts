import os
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--root", type=str)
parser.add_argument("--weak_in", type=int, default=9)
parser.add_argument("--weak_out", type=int, default=795)
args = parser.parse_args()

# root="/data/users/Aurelio/fermi"
root=args.root
gtselect_utils_path = f"{root}/utils/"
os.makedirs(gtselect_utils_path, exist_ok=True)

week_min=args.weak_in
week_max=args.weak_out

with open(f"{gtselect_utils_path}/gtselect_fits.txt", "w") as f:
    for i in range(week_min, week_max+1):
        if i == 512:
            #this week is missing
            continue
        
        f.write(f"{root}/photon/lat_photon_weekly_w{i:03d}_p305_v001.fits \n")

