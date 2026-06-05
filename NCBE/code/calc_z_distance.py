#!/usr/bin/env python3

import csv
import argparse
import numpy as np


def parse_pdb_models(pdb_file):
    """
    读取多模型 PDB 文件。
    返回:
        models: list of dict
        每一帧是一个字典，key = (resname, resid), value = np.array([x, y, z])
    """
    models = []
    current_model = {}

    with open(pdb_file, "r") as f:
        for line in f:
            record = line[:6].strip()

            if record == "MODEL":
                if current_model:
                    models.append(current_model)
                    current_model = {}

            elif record == "ATOM":
                atom_name = line[12:16].strip()
                resname = line[17:20].strip()
                resid = int(line[22:26].strip())
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())

                if atom_name == "CA":
                    current_model[(resname, resid)] = np.array([x, y, z], dtype=float)

            elif record == "ENDMDL":
                if current_model:
                    models.append(current_model)
                    current_model = {}

        # 防止最后一帧没有 ENDMDL
        if current_model:
            models.append(current_model)

    return models


def main():
    parser = argparse.ArgumentParser(
        description="Calculate per-frame Z-axis distance between two CA atoms from a multi-model PDB trajectory."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input multi-model PDB file"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output CSV file"
    )
    parser.add_argument(
        "--res1",
        type=int,
        required=True,
        help="Residue ID of the first CA atom"
    )
    parser.add_argument(
        "--res2",
        type=int,
        required=True,
        help="Residue ID of the second CA atom"
    )
    parser.add_argument(
        "--resname1",
        type=str,
        default=None,
        help="Residue name of the first atom, e.g. GLU"
    )
    parser.add_argument(
        "--resname2",
        type=str,
        default=None,
        help="Residue name of the second atom, e.g. GLU"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print per-frame Z-distance information"
    )

    args = parser.parse_args()

    pdb_file = args.input
    output_csv = args.output

    models = parse_pdb_models(pdb_file)

    results = []

    for i, model in enumerate(models, start=1):
        # 如果用户指定了 resname，就按 (resname, resid) 找
        # 否则就按 resid 模糊匹配
        if args.resname1:
            key1 = (args.resname1.upper(), args.res1)
            atom1 = model.get(key1, None)
        else:
            matches1 = [coord for (resname, resid), coord in model.items() if resid == args.res1]
            atom1 = matches1[0] if len(matches1) == 1 else None

        if args.resname2:
            key2 = (args.resname2.upper(), args.res2)
            atom2 = model.get(key2, None)
        else:
            matches2 = [coord for (resname, resid), coord in model.items() if resid == args.res2]
            atom2 = matches2[0] if len(matches2) == 1 else None

        if atom1 is None or atom2 is None:
            print(f"Frame {i}: cannot find specified atoms, skipped.")
            continue

        z1 = atom1[2]
        z2 = atom2[2]

        dz_signed = z2 - z1
        dz_abs = abs(dz_signed)

        results.append([i, z1, z2, dz_signed, dz_abs])

        if args.verbose:
            print(
                f"Frame {i}: z1 = {z1:.6f}, z2 = {z2:.6f}, "
                f"dz = {dz_signed:.6f}, |dz| = {dz_abs:.6f}"
            )

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Frame", "Z1", "Z2", "Delta_Z", "Abs_Delta_Z"])
        writer.writerows(results)

    print(f"Processed {len(results)} frames.")
    print(f"Saved to: {output_csv}")


if __name__ == "__main__":
    main()
