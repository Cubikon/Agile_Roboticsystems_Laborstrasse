## TODO
## Ujwal Subedi
1. [ ] Code Cleanup & Code Comments
2. [ ] PC Transformer2023 Prio 1
3. [ ] Relative Folder Structure fix for Labor PC
4. [ ] Layout View for Experiment, Plasmid, Tubes using Mock Data
5. [ ] Export of Data , downloadable Excel File
6. [ ] update README 

## Wissam Alamareen
1. [ ] Return all Experiments of a Labor Assistant using laborant id

## Completed Tasks
### Ujwal Subedi
1. [x] Display QR code Image in UI
2. [x] Standard Error/Output/input (stdout stderr stdin) displayed in a window on GUI
3. [x] QR Code Generator Layout in UI
4. [x] Navigation Left Menu Layout
5. [x] Cross-process communication
6. [x] Added Experiment Tubes Table to show Experiment Info about Current Experiment
7. [x] Added Json-based Application Caching to Save previous application data for the startup
    - Loads Experiment Tubes Information of Previous Experiment on Startup
    - Loads QR-Codes of Previous Experiment on Startup
8. [x] Implement Borg Singleton for Runtime shared cache
9. [x] Experiment Preparation with multiple Page System 
    - Experiment Creation / Import
    - Show all the provided Plasmid Nr as a List 
        -  Show Input Field for each Plasmid Nr to accept Tube Nr in comma separated List eg. (5,7,8,12,24)
10. [x] Adding filter to Experiment Creation Form
11. [x] Redesign QR-Image view row list near Experiment Tubes view

## Completed Tasks
### Wissam Alamareen
1. [x] Experiment creation or import
2. [x] Check if Experiment Exists
3. [x] Import of Plasmid metadata
4. [x] List of Tubes creation with Plasmid and Experiment ID
    - [x] QR Code Generation and assign it to Tube
5. [x] Return Experiment Data of a specific Experiments using Experiment Id
6. [x] Return Number of Experiments of a Labor Assistant using their Name
7. [x] Return all Tubes of specific Experiments using Experiment Id
8. [x] Return Tube Data per probe_ne(id)
9. [x] Return plasmid Data per plasmid_nr(id)
10. [x] Return all Tubes data of specific Experiment
11. [x] Return all Experiments of a Labor Assistant using laborant id


## On Progress
### Ujwal Subedi
1. Redesign QR-Image view row list near Experiment Tubes view


### TODO
### Wissam Alamareen


### Process for Labor Assistant
- Experiment Preparation
  - Enter Experiment Id, Name, Lastname ,Nr of Plasmid, Nr of Tubes, List of Plasmid in comma separated text eg. (2,5,6,4)
  - Enter List of Tubes (Probe Nr) in comma separated text
  - View List of QR Codes and Probe Nr 
    - Print QR Code Image 
  - Start Monitoring Application
