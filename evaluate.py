import os
import math
import csv
import argparse
import numpy as np
import torch
from scipy.spatial.transform import Rotation
from robustRotationEstimator import RobustRotationEstimator


def load(sequence_path: str):
    """
    Load a sequence of the BUSS dataset
    :param sequence_path: Path to the BUSS sequence
    :return: Dict
    """

    # Ground truth rotations
    rotations = []
    # Optical flows
    flows = []

    with open(os.path.join(sequence_path, 'rotations.csv'), mode='r') as rotations_file:

        for i, line in enumerate(csv.reader(rotations_file)):
            if i == 0:
                continue

            quat = [float(e) for e in line]
            quat[0] = - quat[0]
            quat[1] = - quat[1]

            # Ground truth rotations
            rotations.append(Rotation.from_quat(quat))

            # Flows
            flow_folder = os.path.join(sequence_path, 'flows_undistorted_4')
            flows.append(torch.load(os.path.join(flow_folder, f'{i - 1:06d}_4.pt')))

    return {
        'flows': flows,
        'rotations': rotations,
    }


def evaluate(buss_path: str):
    """
    Evaluate on BUSS dataset
    :param buss_path: Path to the BUSS dataset
    """
    rotation_estimator = RobustRotationEstimator(
        h=270,
        w=480,
        f=1655 / 4,
        bin_size=0.001,
        max_angle=0.07,
        spatial_step=15)

    errors = []

    for sequence in os.listdir(buss_path):

        sequence_path = os.path.join(buss_path, sequence)
        if os.path.isdir(sequence_path):
            print(f"Evaluating sequence {sequence}")
            data = load(sequence_path)

            assert len(data['flows']) == len(
                data['rotations']), f"Expected {len(data['flows'])} == {len(data['rotations'])}"

            for i, flow in enumerate(data['flows']):
                rot_est = -rotation_estimator.estimate(flow)
                # rot_est[2] = -rot_est[2]
                errors.append((Rotation.from_rotvec(rot_est).inv() * data['rotations'][i]).magnitude())

    errors = np.array(errors)
    print(f"Average error in deg: {errors.sum() / len(errors) / math.pi * 180}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--buss_path', type=str, required=True, help="Path to the buss dataset")
    args = parser.parse_args()

    evaluate(args.buss_path)
