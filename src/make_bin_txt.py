#%%
import os
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--root", type=str)
parser.add_argument("--Emin", type=int, default=1_000)
parser.add_argument("--Emax", type=int, default=10_000)
parser.add_argument("-n", "--nbins", type=int, default=10)
parser.add_argument("--ebins", type=str, default=None)
args = parser.parse_args()

root=args.root
utils_path = f"{root}/utils/"
os.makedirs(utils_path, exist_ok=True)

nbins=args.nbins
if args.ebins is None or args.ebins == "None":
    print(f"Using {nbins} bins from Emin and Emax")
    Emin=args.Emin # MeV
    Emax=args.Emax # MeV
    Earr = np.logspace(np.log10(Emin), np.log10(Emax), nbins+1)
else:
    print(f"Using ebins, with {nbins} bins per energy bin: {args.ebins}")
    ebins = [float(x) for x in args.ebins.split(" ")]
    Earr = np.array([])
    for i in np.arange(len(ebins)-1):
        Earr_bin = np.logspace(np.log10(ebins[i]), np.log10(ebins[i+1]), nbins+1)
        Earr = np.append(Earr, Earr_bin[:-1])
        if i == len(ebins)-2:
            Earr = np.append(Earr, Earr_bin[-1])


with open(f"{utils_path}/ebins.txt", "w") as f:
    for i in np.arange(len(Earr)-1):
        f.write(f"{Earr[i]:.6f} {Earr[i+1]:.6f}\n")
