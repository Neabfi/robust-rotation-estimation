import argparse
import numpy as np
from robustRotationEstimator import RobustRotationEstimator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--flow', type=str, required=True, help="Path to optical flow")
    parser.add_argument('--f', type=float, default=1655 / 4, help="Focal length")

    parser.add_argument('--spatial_step', type=int, default=15, help="Flow grid sample rate")
    parser.add_argument('--bin_size', type=float, default=0.001, help="Size of the rotation bins in radian")
    parser.add_argument('--max_angle', type=float, default=0.07, help="Range of rotations to search for in radian. The rotation will be searched within [-max_angle, max_angle]")
    args = parser.parse_args()

    flow = np.load(args.flow)

    # Frame size
    h, w, _ = flow.shape

    # Focal length
    f = 1655 / 4

    rotation_estimator = RobustRotationEstimator(
        h,
        w,
        args.f,
        args.bin_size,
        args.max_angle,
        args.spatial_step)

    rot_est = rotation_estimator.estimate(flow)

    print(f"Estimated rotation:", rot_est)
