# Optical Detection of Electron Spin Resonance in NV⁻ Centres

This repository contains the code and documentation for running a compact ODMR (Optically Detected Magnetic Resonance) platform on nitrogen-vacancy (NV⁻) centres in microdiamonds. The platform uses laser excitation, microwaves, and synchronized photodetection to resolve zero-field and Zeeman-split spin transitions in diamond NV⁻ centres.

---

## 🔬 Project Summary

Negatively charged NV⁻ centres in diamond exhibit spin-dependent fluorescence under optical excitation and microwave driving. In this project, I built a tabletop system to:

- Resolve zero-field ESR transitions (~2.87 GHz).
- Detect Zeeman splitting under external magnetic fields.
- Synchronize data acquisition with a custom Python script.

We show that even using modest, off-the-shelf optomechanical equipment, we can exert quantum control in solid state systems.

**Key hardware**:  
- SG4400L RF Signal Generator (DS Instruments)
- Thorlabs SPCM20A Single-Photon Detector (Thorlabs)
- Moku:Lab Oscilloscope (Liquid Instruments)
- Neodymium magnet (~2.6 mT)

---

## ⚙️ System Overview

The experiment setup includes:
- A 532 nm laser diode.
- Optomechanics for beam shaping and focusing.
- Dichroic lenses and filters for fluorescence detection.
- Microwave delivery via PCB stripline (rigged up by Dr. Cyril Laplane).
- Python-based serial control of RF source and data acquisition.

Please see the report for the detailed optomechanical layout.

---

## 🧠 Code Features

- `frequency_sweep_experiment.py`: Automates RF frequency sweep, toggling microwaves, and capturing photon counts with real-time plotting and saving of experimental data. Script is available [here](./src/frequency_sweep_experiment.py)

---

## 📊 Sample Output

Sample real-time plot from the experiment automation script is available [here](./data/1MHzsweep_100steps_10bins.png)

---

## 📁 Folder Structure

- `src/`: Source code
- `data/`: Sample real-time plot that is produced by the source code
- `report/': Final report for SCDL3991 - Science Dalyell Individual Research Project

---

## 📜 Report

The full technical report is available [here](./report/Yunki_Dalyell_Report_23JUNE25.pdf) 

---

## 🧑‍💻 Author

**Yunki Yau**  
- University of Sydney, BSc(Adv) Physics major (complete) & Computer Science minor (1st year), Dalyell Scholar Program
- Email: yyau2516@uni.sydney.edu.au, yunki.yau@gmail.com

---

## 🧪 Acknowledgements

Supervised by Dr. Robert Wolf and Dr. Cyril Laplane (USyd Quantum Control Lab).

> ⚠️ This project was conducted under supervision at the University of Sydney Quantum Control Laboratory.  
> Code and documentation are shared for academic review and demonstration purposes only.  
> Please contact me (yyau2516@uni.sydney.edu.au or yunki.yau@gmail.com) before reusing or redistributing any portion of this work.


