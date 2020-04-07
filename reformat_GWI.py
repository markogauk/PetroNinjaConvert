import pandas as pd
import os
import tkinter 
from tkinter import messagebox
from tkinter import filedialog

def folder_Window():
    #initiate tinker and hide window 
    main_win = tkinter.Tk() 
    main_win.withdraw()

    main_win.overrideredirect(True)
    main_win.geometry('0x0+0+0')

    main_win.deiconify()
    main_win.lift()
    main_win.focus_force()

    #open file selector 
    main_win.sourceFile = filedialog.askdirectory(parent=main_win, initialdir= "\\",title='Please select a directory')

    #close window after selection 
    main_win.destroy()

    return main_win.sourceFile

def gwiFormat(convert_dir):
    
    file_list = os.listdir(convert_dir)

    # Load in file with well_details in the name
    well_GWI = [x for x in file_list if 'well_details' in x]

    # Create list of headers compatible with SeisWare
    GWI_header_list = ['Common Well Name','UWI','Fluid','Current Status','Bottom Latitude','Bottom Longitude',
    'Spud Date','Ground Elevation','KB','Rig Release Date','TVD','Total Depth','Province/State','Field','Surface Latitude','Surface Longitude']

    # Read the file, select only the necessary columns, rename the columns as intended
    gwi_DF = pd.read_csv(convert_dir + '/' + well_GWI[0],usecols=[0,1,2,3,5,6,7,11,12,18,19,20,22,23,36,37],header=0,names=GWI_header_list)

    # Write the dataframe out to a CSV
    gwi_DF.to_csv(convert_dir + '/' + 'wellGWI_SW.csv', index = False)

    # Output a dictionary of UWI : Producing Formation
    prodmap_DF = pd.read_csv(convert_dir + '/' + well_GWI[0])
    prod_dict = dict(zip(prodmap_DF.wellbore_uwi, prodmap_DF.formation))

    return prod_dict

def dirFormat(convert_dir):

    file_list = os.listdir(convert_dir)

    # Load in the file with directionals in the name
    well_dir = [x for x in file_list if 'directionals' in x]

    # Create list of header compatible with SeisWare
    dir_header_list = ['UWI','Measured Depth','Inclination','Azimuth']

    # Read the file, select only the necessary columns, rename the columns as intended
    dir_DF = pd.read_csv(convert_dir + '/' + well_dir[0],usecols=[0,1,3,4],header=0,names=dir_header_list)

    # Write the dataframe out to a CSV
    dir_DF.to_csv(convert_dir + '/' + 'welldirSW.csv', index = False)

    return

def topsFormat(convert_dir):

    file_list = os.listdir(convert_dir)

    # Load in the file with formations in the name   
    well_tops = [x for x in file_list if 'formations' in x]

    # Create list of header compatible with SeisWare
    top_header_list = ['UWI','Formation Top Depth','Formation ID']

    # Read the file, select only the necessary columns, rename the columns as intended
    top_DF = pd.read_csv(convert_dir + '/' + well_tops[0],usecols=[0,1,3],header=0,names=top_header_list)

    # Write the dataframe out to a CSV
    top_DF.to_csv(convert_dir + '/' + 'welltopSW.csv', index = False)

    return

def prodFormat(convert_dir,prod_dict):
    
    file_list = os.listdir(convert_dir)

    # Load in the file with production in the name
    well_prod = [x for x in file_list if 'production' in x]

    # Create list of header compatible with SeisWare
    prod_header_list = ['UWI',"Production Volume Date","Oil Monthly Production","Gas Monthly Production","Water Monthly Production","Water Monthly Injection","Time On - Production Hours","Time On - Injection Hours"]

    # Read in the file to a dataframe
    prod_DF = pd.read_csv(convert_dir + '/' + well_prod[0],usecols=[0,1,2,3,4,5,10,11],header=0,names=prod_header_list)

    # Add a column for production entity using the formation from the well details
    prod_DF['Formation'] = prod_DF['UWI'].map(prod_dict)

    # Output to csv file
    prod_DF.to_csv(convert_dir + '/' + 'wellprodSW.csv', index = False)

    return prod_DF

def main():
    
    # Set the folder for the files
    convert_dir = folder_Window()

    prod_dict = gwiFormat(convert_dir)

    topsFormat(convert_dir)

    dirFormat(convert_dir)

    prodFormat(convert_dir,prod_dict)

if __name__ == "__main__":
    main()



