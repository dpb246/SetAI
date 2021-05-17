#small script to create all the folders for the dataset
import os

dir_path = r"C:\Users\dpb24\OneDrive - University of Waterloo\SideProjects\SetGame\Images"



for colour in ["orange", "green", "pink"]:
    for shape in ["diamond", "oval", "squiggle"]:
        for count in range(1, 4):
            for shading in ["outline", "shaded", "filled"]:
                path = os.path.join(dir_path, f"{colour}-{count}-{shape}-{shading}")
                os.mkdir(path)



