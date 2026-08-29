# 🌍 USCS Soil Classification Tool

A desktop application and dataset for classifying soils according to the **Unified Soil Classification System (USCS)** — built with Python, Tkinter, and Matplotlib. The tool takes standard geotechnical lab inputs (sieve analysis and Atterberg limits) and returns the USCS group symbol, description, and an interactive Casagrande Plasticity Chart.


---

## 📖 Overview

Soil classification is a foundational step in geotechnical engineering, used to assess bearing capacity, permeability, compressibility, and suitability for construction. This repository provides:

1. **`soil_gui.py`** — an interactive desktop GUI that classifies a soil sample and plots it on the Casagrande Plasticity Chart.
2. **A labeled reference dataset** (`Dataset.csv` / `USCS_soil_classification_dataset_240_samples.xlsx`) of 240 synthetic soil samples spanning all 12 major USCS groups — ideal for testing, benchmarking, or training ML classifiers.

---

## ✨ Features

- **Instant USCS classification** from four lab inputs: % passing 0.075 mm sieve, % passing 4.75 mm sieve, Liquid Limit (LL), and Plastic Limit (PL).
- **Automatic PI and A-Line computation**, using the standard Casagrande A-line equation: `A-line PI = 0.73 × (LL − 20)`.
- **Fine-grained and coarse-grained soil logic**:
  - Fine-grained (fines > 50%): distinguishes `CL`, `ML`, `CH`, `MH` based on LL and the A-line.
  - Coarse-grained (fines ≤ 50%): distinguishes gravel (`G`) vs. sand (`S`) base symbols, and clean/silty/clayey/dual-symbol cases based on fines content.
- **Casagrande Plasticity Chart plotting** via Matplotlib — visualizes where the sample falls relative to the A-line.
- **Input validation** with friendly error dialogs for out-of-range or inconsistent values (e.g., PL > LL).
- **Reference dataset** of 240 pre-labeled samples across 12 USCS groups (GW, GP, GM, GC, SW, SP, SM, SC, ML, CL, MH, CH), pre-split into Train/Test/Validation sets.

---

## 🗂️ Repository Structure

```
.
├── soil_gui.py                                     # Tkinter GUI application
├── Dataset.csv                                     # 240-sample labeled soil dataset (CSV)
├── USCS_soil_classification_dataset_240_samples.xlsx  # Same dataset (Excel)
└── README.md
```

---

## 🧪 Dataset

`Dataset.csv` contains 240 synthetically generated soil samples, 20 per USCS group, with the following columns:

| Column | Description |
|---|---|
| `Sample_ID` | Unique sample identifier |
| `USCS_Label` | Ground-truth USCS group symbol (GW, GP, GM, GC, SW, SP, SM, SC, ML, CL, MH, CH) |
| `Fines_Passing_0.075mm_pct` | % passing the No. 200 sieve (fines content) |
| `Passing_4.75mm_pct` | % passing the No. 4 sieve |
| `D10_mm`, `D30_mm`, `D60_mm` | Grain diameters at 10%, 30%, and 60% passing |
| `Cu` | Coefficient of uniformity |
| `Cc` | Coefficient of curvature |
| `Liquid_Limit_LL` | Liquid limit (%) |
| `Plastic_Limit_PL` | Plastic limit (%) |
| `Plasticity_Index_PI` | LL − PL |
| `Dataset_Split` | Pre-assigned `Train` / `Test` / `Validation` split |

**Class balance:** 20 samples per class across all 12 groups.
**Split:** 168 Train / 36 Test / 36 Validation.

This dataset is well suited for training and evaluating supervised ML classifiers (decision trees, random forests, SVMs, neural nets) as an alternative or complement to the rule-based classifier in `soil_gui.py`.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- `tkinter` (usually bundled with Python; on Linux install via `sudo apt-get install python3-tk` if missing)
- `matplotlib`

### Installation

```bash
git clone https://github.com/<your-username>/uscs-soil-classification.git
cd uscs-soil-classification
pip install matplotlib
```

### Run the GUI

```bash
python soil_gui.py
```

---

## 🖥️ Usage

1. Launch the app with `python soil_gui.py`.
2. Enter the four required lab values:
   - **% Passing 0.075 mm** (fines content)
   - **% Passing 4.75 mm**
   - **Liquid Limit (LL)**
   - **Plastic Limit (PL)**
3. Click **Classify Soil** to view:
   - Plasticity Index (PI)
   - A-Line PI
   - Soil type (Fine-Grained / Coarse-Grained)
   - USCS group symbol
   - Plain-language description
4. Click **Show Plasticity Chart** to plot the sample's (LL, PI) point against the A-line on a Casagrande chart.

### Example

| Input | Value |
|---|---|
| % Passing 0.075 mm | 60 |
| % Passing 4.75 mm | 90 |
| Liquid Limit | 45 |
| Plastic Limit | 25 |

**Output:** `PI = 20.00`, `A-Line PI = 18.25` → `Type = Fine Grained Soil`, `Group = CL`, `Description = Lean Clay`

---

## 🧠 Classification Logic

The classifier follows a simplified version of the ASTM D2487 USCS flowchart:

```
                         % Fines (passing No.200)
                                   │
                 ┌─────────────────┴─────────────────┐
              > 50%                                ≤ 50%
        Fine-Grained Soil                    Coarse-Grained Soil
                 │                                     │
        ┌────────┴────────┐              % passing No.4 → Gravel (G) / Sand (S)
      LL < 50            LL ≥ 50                        │
   ┌────┴────┐        ┌────┴────┐        ┌──────────────┼──────────────┐
PI≥A-line  PI<A-line PI≥A-line PI<A-line  Fines<5%    5–12%          Fines≥12%
   CL         ML        CH        MH      Clean(*)   Dual symbol(*)  PI≥A-line → C
                                                                       PI<A-line → M
```

> ⚠️ **Note:** Cases with 0–12% fines in coarse-grained soils require gradation parameters (Cu, Cc) for a definitive dual symbol (e.g., `GW-GC`), which this tool flags but does not fully resolve — see [Limitations](#-limitations--roadmap).

---

## ⚠️ Limitations & Roadmap

- [ ] Incorporate `Cu`/`Cc` gradation checks (already present in the dataset) to fully resolve clean (`GW`/`GP`/`SW`/`SP`) and dual-symbol (`GW-GC`, `SP-SM`, etc.) classifications.
- [ ] Add unit tests validating the rule-based classifier against the 240-sample dataset.
- [ ] Train and compare an ML classifier (e.g., Random Forest) on the dataset against the rule-based approach.
- [ ] Package as a standalone executable (PyInstaller) for non-technical users.
- [ ] Add organic soil (`OL`/`OH`/`Pt`) detection.
- [ ] Migrate GUI to a modern framework (e.g., PyQt or a web app) for improved UX.

---





---

## 🙏 Acknowledgments

- Classification logic based on **ASTM D2487** — Standard Practice for Classification of Soils for Engineering Purposes (Unified Soil Classification System).
- Built with [Tkinter](https://docs.python.org/3/library/tkinter.html) and [Matplotlib](https://matplotlib.org/).
