# NND Analysis — Tumor–T Cell Nearest Neighbor Distance

A lightweight Python script to compute the **nearest neighbor distance (NND)** between tumor cells and T cells from 2D centroid coordinates exported by [TrackMate](https://imagej.net/plugins/trackmate/) (Fiji/ImageJ).

For each tumor cell, the script computes the Euclidean distance to every T cell in the same field and keeps the minimum, providing a per-cell measure of spatial proximity to the nearest T cell. The analysis is run separately on paired timepoints (e.g. start and end of an intravital imaging acquisition) to track changes in tumor–T cell spatial relationships over time.

## Requirements

- Python ≥ 3.8
- `numpy`
- `pandas`
- `tkinter` (included in most standard Python installations; on Linux may require `python3-tk`)

Install dependencies:
```bash
pip install numpy pandas
```

## Input format

Four CSV files are required, two per timepoint:

| File | Content |
|---|---|
| Tumor (start) | Tumor cell centroids at frame 0 |
| T cells (start) | T cell centroids at frame 0 |
| Tumor (end) | Tumor cell centroids at the final frame |
| T cells (end) | T cell centroids at the final frame |

Each CSV must contain at least the columns `X` and `Y` (centroid coordinates), consistent with a standard TrackMate spot export.

## Usage

Run the script from the command line:
```bash
python nnd_analysis.py
```

A file dialog will prompt you to select, in order:
1. Tumor CSV (start)
2. T cell CSV (start)
3. Tumor CSV (end)
4. T cell CSV (end)

## Output

Two annotated CSV files are saved in the same directory as the input files:

- `distances_start.csv`
- `distances_end.csv`

Each is a copy of the corresponding tumor cell file with an added column:

- `min_dist_to_T`: Euclidean distance (in the original coordinate units, typically pixels or µm depending on TrackMate calibration) from each tumor cell to its nearest T cell.

## Citation

If you use this script, please cite our paper.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
