import random
import numpy as np
import torch
from track_dataset import run

random.seed(42)
np.random.seed(42)
torch.random.manual_seed(42)


def main(algorithm_name, experts, dataset_name, **kargs):
    n_experts = len(experts)
    mode = kargs["mode"]
    if algorithm_name == "AAA":
        from algorithms.aaa import AAA

        algorithm = AAA(n_experts, **kargs)
    elif algorithm_name == "Average":
        from algorithms.average import Average

        algorithm = Average(n_experts, mode)
    elif algorithm_name == "MCCT":
        from algorithms.mcct import MCCT

        algorithm = MCCT(n_experts, mode)
    elif algorithm_name == "Max":
        from algorithms.baseline import Baseline

        algorithm = Baseline(
            n_experts, name=f"Max_{mode}", use_iou=False, use_feature=True
        )
    elif algorithm_name == "Random":
        from algorithms.random import Random

        algorithm = Random(n_experts, mode)
    else:
        raise ValueError("Unknown algorithm name")

    run(algorithm, dataset_name, experts=experts)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithm", default="AAA", type=str)
    parser.add_argument("-e", "--experts", default=list(), nargs="+")
    parser.add_argument("-d", "--dataset", default="OTB", type=str)
    parser.add_argument("-n", "--mode", default="Expert", type=str)
    parser.add_argument("-t", "--iou_threshold", default=0.0, type=float)
    parser.add_argument("-r", "--feature_threshold", default=0.0, type=float)
    parser.add_argument("-s", "--reset_target", action="store_true")
    parser.add_argument("-m", "--only_max", action="store_true")
    parser.add_argument("-i", "--use_iou", action="store_true")
    parser.add_argument("-f", "--use_feature", action="store_false")
    parser.add_argument("-x", "--cost_iou", action="store_false")
    parser.add_argument("-y", "--cost_feature", action="store_false")
    parser.add_argument("-z", "--cost_score", action="store_false")
    args = parser.parse_args()

    main(
        args.algorithm,
        args.experts,
        args.dataset,
        mode=args.mode,
        iou_threshold=args.iou_threshold,
        feature_threshold=args.feature_threshold,
        reset_target=args.reset_target,
        only_max=args.only_max,
        use_iou=args.use_iou,
        use_feature=args.use_feature,
        cost_iou=args.cost_iou,
        cost_feature=args.cost_feature,
        cost_score=args.cost_score,
    )