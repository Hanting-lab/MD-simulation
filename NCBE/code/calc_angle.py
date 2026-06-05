#!/usr/bin/env python3

import math
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


def midpoint(p1, p2):
    return (p1 + p2) / 2.0


def calc_angle(a, b, c):
    """
    计算 ∠acb，即向量 CA 和 CB 的夹角
    顶点在 c
    """
    v1 = a - c   # CA
    v2 = b - c   # CB

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return np.nan

    cos_theta = np.dot(v1, v2) / (norm1 * norm2)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    angle_rad = math.acos(cos_theta)
    return math.degrees(angle_rad)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate per-frame angle ∠acb from a multi-model PDB trajectory."
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
        "-v", "--verbose",
        action="store_true",
        help="Print per-frame angle information"
    )

    args = parser.parse_args()

    pdb_file = args.input
    output_csv = args.output

    models = parse_pdb_models(pdb_file)

    # 残基定义
    key_E533 = ("GLU", 533)
    key_K577 = ("LYS", 577)
    key_R622 = ("ARG", 622)
    key_E639 = ("GLU", 639)
    key_K643 = ("LYS", 643)

    results = []

    for i, model in enumerate(models, start=1):
        required_keys = [key_E533, key_K577, key_R622, key_E639, key_K643]
        missing = [key for key in required_keys if key not in model]

        if missing:
            print(f"Frame {i}: missing residues {missing}, skipped.")
            continue

        # a点 = E639 和 K643 的中点
        a = midpoint(model[key_E639], model[key_K643])

        # b点 = E533 和 K577 的中点
        b = midpoint(model[key_E533], model[key_K577])

        # c点 = R622
        c = model[key_R622]

        angle = calc_angle(a, b, c)
        results.append([i, angle])

        if args.verbose:
            print(f"Frame {i}: angle = {angle:.6f} deg")

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Frame", "Angle_deg"])
        writer.writerows(results)

    print(f"Processed {len(results)} frames.")
    print(f"Saved to: {output_csv}")


if __name__ == "__main__":
    main()
