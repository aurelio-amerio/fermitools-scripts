import os
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--root", type=str)
parser.add_argument("--weak_in", type=int, default=9)
parser.add_argument("--weak_out", type=int, default=795)
args = parser.parse_args()

# root="/data/users/Aurelio/fermi"
root=args.root
gtmktime_utils_path = f"{root}/utils/"
os.makedirs(gtmktime_utils_path, exist_ok=True)

week_min=args.weak_in
week_max=args.weak_out

with open(f"{gtmktime_utils_path}/spacecraft_list.txt", "w") as f:
    for i in range(week_min, week_max+1):
        if i == 512:
            #this week is missing
            continue
        
        f.write(f"{root}/spacecraft/lat_spacecraft_weekly_w{i:03d}_p310_v001.fits \n")

