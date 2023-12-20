# Statistical Complexity of Insight Meditation

## Overview
This project uses the complexity code published by Starkey et al. applied to EEG recordings provided by the meditation expert Daniel Ingram, author of ["Mastering the Core Teachings of the Buddha"](https://www.mctb.org/) and now with the [EPRC](https://theeprc.org/) working to add spiritual measurements to the DSM. The purpose of this new complexity measurement is "constructing an equation that can measure and describe the richness of conscious experience in any physical system, whether human, animal, or machine" [Study link](https://www.vox.com/future-perfect/2023/12/15/24001424/consciousness-complexity-neuroscience-mental-health). The authors explain that this new measurement does not succeed in this grand ambition, but it is a bit closer. Looking at the results of this measurement when applied to Daniel's meditation data, it does look they are on the right track. Complexity increases dramatically in the same way during each of his recorded meditation sessions, while control data doesn't show any similar increase. We hope this data helps guide the development of this helpful measurement.


- [Study link](https://www.biorxiv.org/content/10.1101/2023.12.05.570101v1)
- [Vox article](https://www.vox.com/future-perfect/2023/12/15/24001424/consciousness-complexity-neuroscience-mental-health)
- [Study code](https://github.com/CDR-Clueless/Statistical-Complexity)
- [Daniel's EEG data](https://osf.io/srfnz/?view_only=1a408d6b96a6402bbf1464418ec3219e)


## Results

Every meditation session Daniel record shows similar complexity behavior: a stead rise at the same rate every session, levelling out at the the same range. Compared with a control session the differences are clear. In the control, Daniel recorded with closed eyes and calm focus but not attempt at insight for the for the first 20 minutes:

![All meditation sessions with control](images/Meditation_vs_Control.png)

## Code

Complexity is calculated from the raw EEG voltages extracted from .EEG files provided by Daniel here (link at top of this page). Voltage files are large (>200mb), so only one file is provided in this repository as an example, found in the 'Example' folder. Complexity can be calculated from the python file in this same folder:

```bash
python3 calculate_complexity.py 'August 20 - Raw Voltages.csv' 

```

This code plots the complexity for each EEG electrode, then saves a CSV file with the data as 'complexity_scores.csv', which is also included in this folder. The complexity code is verbatim what Starkey et al provided - they thoughtfully included binarizing function which accepts an array of floats, which in this case is simply a 10-second segment of raw EEG data. No modification of the code was necessary to get this working, except to loop over the raw data in 10-second windows and save each result to a new array for plotting and exporting.

Plotting the Meditation vs Control graph is provided in the 'Combined Averages' folder. 'Complexity_with_Control.csv' combines the average complexity score of all EEG locations at each moment into a single average for each meditation session. A 'Control' column at the end does the same for Daniel's control session.

Extracting raw voltages from .EEG files hosted by Daniel can be done with the 'Extract_Raw_Volts.py'. This requires a folder with .EEG and .VHDR files. The extracted CSV will have the raw volts for each EEG sensor, at 500hz sample rate.