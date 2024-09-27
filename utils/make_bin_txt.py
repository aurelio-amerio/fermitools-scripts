#%%
import os
import numpy as np

class make_bin_txt():
    def __init__(self, root, Emin=None, Emax=None, ebins=None, nbins=None):
        self.utils_path = f"{root}/utils/"
        os.makedirs(self.utils_path, exist_ok=True)
        self.nbins = nbins

        if ebins is None:
            assert Emin is not None and Emax is not None, "Emin and Emax must be specified if ebins is None"
            print(f"Using {nbins} bins from Emin and Emax")
            self.Earr = np.logspace(np.log10(Emin), np.log10(Emax), nbins+1)
        else:
            assert nbins is not None, "nbins must be specified if ebins is not None"
            print(f"Using ebins, with {nbins} bins per energy bin: {ebins}")
            self.Earr = np.array([])
            for i in np.arange(len(ebins)-1):
                Earr_bin = np.logspace(np.log10(ebins[i]), np.log10(ebins[i+1]), nbins+1)
                self.Earr = np.append(self.Earr, Earr_bin[:-1])
                if i == len(ebins)-2:
                    self.Earr = np.append(self.Earr, Earr_bin[-1])

        return

    def write(self):
        with open(f"{self.utils_path}/ebins.txt", "w") as f:
            for i in np.arange(len(self.Earr)-1):
                f.write(f"{self.Earr[i]:.6f} {self.Earr[i+1]:.6f}\n")
        return
    



