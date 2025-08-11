# Optical Detection of Electron Spin Resonance in NV⁻ Centres

This repository contains the code and documentation for a compact ODMR (Optically Detected Magnetic Resonance) platform using nitrogen-vacancy (NV⁻) centres in microdiamonds. The platform integrates optical excitation, microwave control, and synchronized photodetection to resolve zero-field and Zeeman-split spin transitions.

---

## 🔬 Project Summary

Negatively charged NV⁻ centres in diamond exhibit spin-dependent fluorescence under optical excitation and microwave driving. In this project, I built a tabletop system to:

- Resolve zero-field ESR transitions (~2.87 GHz).
- Detect Zeeman splitting under external magnetic fields.
- Synchronize data acquisition with a custom Python script.

**Key hardware**:  
- SG4400L RF Signal Generator (DS Instruments)
- Thorlabs SPCM20A Single-Photon Detector (Thorlabs)
- Moku:Lab Oscilloscope (Liquid Instruments)
- Neodymium magnet (~2.6 mT max)

---

## ⚙️ System Overview

The experiment setup includes:
- Laser excitation at 532 nm.
- Optomechanics for beam shaping and focusing.
- Dichroic optics and filters for fluorescence detection.
- Microwave delivery via PCB stripline (rigged up by Dr. Cyril Laplane).
- Python-based serial control of RF source and data acquisition.

Please see the report for the detailed optomechanical layout.

---

## 🧠 Code Features

- `main_control.py`: Automates RF frequency sweep, toggling microwaves, and capturing photon counts.
- `serial_interface.py`: Handles communication with SG4400L and Moku:Lab.
- `signal_processing.py`: Extracts resonance dips, normalizes signal, and plots ODMR spectra.

---

## 📊 Sample Output

Sample output from the code is available [here](./1MHz_sweep_10dbm.png)

---

## 📁 Folder Structure

- `src/`: Source code
- `data/`: Raw traces or processed CSV data
- `figures/`: Beam profiles, resonance curves
- `requirements.txt`: Python dependencies (e.g., `pyserial`, `numpy`, `matplotlib`, `pymoku`)

---

## 📜 Publication / Report

The full technical report is available [here](./Yunki_Dalyell_Report_23JUNE25.pdf) 

---

## 🧑‍💻 Author

**Yunki Yau**  
- University of Sydney, Dalyell Scholar  
- Email: yyau2516@uni.sydney.edu.au  

---

## 🧪 Acknowledgements

Supervised by Dr. Robert Wolf and Dr. Cyril Laplane (USyd Quantum Control Lab).

> ⚠️ This project was conducted under supervision at the University of Sydney Quantum Control Laboratory.  
> Code and documentation are shared for academic review and demonstration purposes only.  
> Please contact me (yunki.yau@gmail.com) before reusing or redistributing any portion of this work.


