import os
# import argparse 

# parser = argparse.ArgumentParser()
# parser.add_argument("-r", "--root", type=str)
# parser.add_argument("--week_in", type=int, default=9)
# parser.add_argument("--week_out", type=int, default=795)
# args = parser.parse_args()

class gtselect_utils():
    def __init__(self, week_min, week_max, root):
        self.week_min = week_min
        self.week_max = week_max
        self.root = root
        self.gtselect_utils_path = f"{root}/utils/"
        os.makedirs(self.gtselect_utils_path, exist_ok=True)
        return
    
    def make_selection_txt(self):
        with open(f"{self.gtselect_utils_path}/gtselect_fits.txt", "w") as f:
            for i in range(self.week_min, self.week_max+1):
                if i == 512:
                    #this week is missing
                    continue
                
                f.write(f"{self.root}/photon/lat_photon_weekly_w{i:03d}_p305_v001.fits \n")
        print("file creted at ", f"{self.gtselect_utils_path}/gtselect_fits.txt")
        return
    
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-r", "--root", type=str)
#     parser.add_argument("--week_in", type=int, default=9)
#     parser.add_argument("--week_out", type=int, default=795)
#     args = parser.parse_args()

#     root=args.root
#     week_min=args.week_in
#     week_max=args.week_out

#     gtselect_utils = gtselect_utils(week_min, week_max, root)
#     gtselect_utils.make_selection_txt()
#     print("done")

