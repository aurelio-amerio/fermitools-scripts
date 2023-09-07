import os
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--root", type=str)
parser.add_argument("--Emin", type=int, default=1_000)
parser.add_argument("--Emax", type=int, default=10_000)
parser.add_argument("-n", "--nbins", type=int, default=10)
args = parser.parse_args()

# root="/data/users/Aurelio/fermi"
root=args.root
utils_path = f"{root}/utils/"
os.makedirs(utils_path, exist_ok=True)

Emin=args.Emin # MeV
Emax=args.Emax # MeV
nbins=10
Earr = np.logspace(np.log10(Emin), np.log10(Emax), nbins+1)
Emin_arr = Earr[:-1]
Emax_arr = Earr[1:]

with open(f"{utils_path}/ebins.txt", "w") as f:
    for i in np.arange(nbins):
        f.write(f"{Emin_arr[i]:.2f} {Emax_arr[i]:.2f}\n")

