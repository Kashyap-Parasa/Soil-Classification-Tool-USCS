import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def classify_soil():
    try:
        fines = float(entry_fines.get())
        passing_475 = float(entry_475.get())
        LL = float(entry_LL.get())
        PL = float(entry_PL.get())

        if not (0 <= fines <= 100 and 0 <= passing_475 <= 100):
            raise ValueError
        if LL < 0 or PL < 0 or PL > LL:
            raise ValueError

        PI = LL - PL
        A_line = 0.73 * (LL - 20)

        # Fine-grained soil
        if fines > 50:
            soil_type = "Fine Grained Soil"

            if LL < 50:
                if PI >= A_line:
                    symbol = "CL"
                    desc = "Lean Clay"
                else:
                    symbol = "ML"
                    desc = "Silt"
            else:
                if PI >= A_line:
                    symbol = "CH"
                    desc = "Fat Clay"
                else:
                    symbol = "MH"
                    desc = "Elastic Silt"

        # Coarse-grained soil
        else:
            soil_type = "Coarse Grained Soil"
            base = "G" if passing_475 < 50 else "S"

            if fines < 5:
                symbol = base + "*"
                desc = "Clean coarse soil; W/P requires gradation (Cu/Cc)"
            elif fines >= 12:
                if PI >= A_line:
                    symbol = base + "C"
                    desc = "Clayey"
                else:
                    symbol = base + "M"
                    desc = "Silty"
            else:
                symbol = base + "*"
                desc = "5–12% fines; dual USCS symbol requires gradation"

        result_label.config(
            text=f"PI = {PI:.2f}\n"
                 f"A-Line PI = {A_line:.2f}\n"
                 f"Type = {soil_type}\n"
                 f"Group = {symbol}\n"
                 f"Description = {desc}"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Enter valid percentages and ensure Plastic Limit <= Liquid Limit."
        )

def plot_chart():
    try:
        LL = float(entry_LL.get())
        PL = float(entry_PL.get())

        if LL < 0 or PL < 0 or PL > LL:
            raise ValueError

        PI = LL - PL
        LL_line = [20, 100]
        PI_line = [0, 0.73 * (100 - 20)]

        plt.figure()
        plt.plot(LL_line, PI_line, label="A-Line")
        plt.scatter(LL, PI)
        plt.xlabel("Liquid Limit")
        plt.ylabel("Plasticity Index")
        plt.title("Casagrande Plasticity Chart")
        plt.grid()
        plt.legend()
        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Enter valid LL and PL values first.")

root = tk.Tk()
root.title("Soil Classification Tool")

tk.Label(root, text="Soil Classification Tool",
         font=("Arial", 16)).pack()

tk.Label(root, text="% Passing 0.075 mm").pack()
entry_fines = tk.Entry(root)
entry_fines.pack()

tk.Label(root, text="% Passing 4.75 mm").pack()
entry_475 = tk.Entry(root)
entry_475.pack()

tk.Label(root, text="Liquid Limit").pack()
entry_LL = tk.Entry(root)
entry_LL.pack()

tk.Label(root, text="Plastic Limit").pack()
entry_PL = tk.Entry(root)
entry_PL.pack()

tk.Button(root, text="Classify Soil",
          command=classify_soil).pack(pady=5)

tk.Button(root, text="Show Plasticity Chart",
          command=plot_chart).pack()

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()
