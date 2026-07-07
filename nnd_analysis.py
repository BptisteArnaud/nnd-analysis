#!/usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox


def compute_min_distances(tumor_df, t_df):
    """
    For each tumor cell, computes the minimal distance (NND) to a T cell.
    Uses the 'X' and 'Y' columns (TrackMate format).
    """
    
    for df, name in [(tumor_df, "tumor cells"), (t_df, "T cells")]:
        if df.empty:
            raise ValueError(f"The {name} file is empty.")
        if "X" not in df.columns or "Y" not in df.columns:
            raise KeyError(f"The {name} file must contain the 'X' and 'Y' columns.")
            
    tumor_coords = tumor_df[["X", "Y"]].to_numpy(float)
    t_coords = t_df[["X", "Y"]].to_numpy(float)
    
    diff = tumor_coords[:, None, :] - t_coords[None, :, :]
    dists = np.sqrt(np.sum(diff ** 2, axis=2))
    min_dists = dists.min(axis=1)
    
    result = tumor_df.copy()
    result["min_dist_to_T"] = min_dists
    return result


def ask_csv(title):
    """Opens a dialog box to select a CSV file."""
    path = filedialog.askopenfilename(
        title=title,
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not path:
        messagebox.showwarning("Cancelled", "Selection cancelled, stopping script.")
        sys.exit(0)
    return path


def main():
    # Initialize Tkinter (no visible main window)
    root = tk.Tk()
    root.withdraw()
    root.update()
    
    # 1. File selection
    tumor_start_path = ask_csv("Select the TUMOR CSV at the START (frame 0)")
    t_start_path = ask_csv("Select the T CELL CSV at the START (frame 0)")
    tumor_end_path = ask_csv("Select the TUMOR CSV at the END (final frame)")
    t_end_path = ask_csv("Select the T CELL CSV at the END (final frame)")
    
    # 2. Read CSV files
    tumor_start = pd.read_csv(tumor_start_path)
    t_start = pd.read_csv(t_start_path)
    tumor_end = pd.read_csv(tumor_end_path)
    t_end = pd.read_csv(t_end_path)
    
    # 3. Compute distances
    debut = compute_min_distances(tumor_start, t_start)
    fin = compute_min_distances(tumor_end, t_end)
    
    # 4. Save results
    out_dir = os.path.dirname(tumor_start_path)
    debut_out = os.path.join(out_dir, "distances_start.csv")
    fin_out = os.path.join(out_dir, "distances_end.csv")
    
    debut.to_csv(debut_out, index=False)
    fin.to_csv(fin_out, index=False)
    
    messagebox.showinfo(
        "Done",
        f"Files saved:\n\n{debut_out}\n{fin_out}"
    )
    root.destroy()
    
if __name__ == "__main__":
    main()
