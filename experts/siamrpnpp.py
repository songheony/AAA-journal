import sys
import cv2
import torch
from base_tracker import BaseTracker
import path_config

sys.path.append("external/pysot")
from pysot.core.config import cfg
from pysot.models.model_builder import ModelBuilder
from pysot.tracker.tracker_builder import build_tracker


class SiamRPNPP(BaseTracker):
    def __init__(self):
        super(SiamRPNPP, self).__init__("SiamRPN++")
        config = path_config.SIAMRPNPP_CONFIG
        snapshot = path_config.SIAMRPNPP_SNAPSHOT

        # load config
        cfg.merge_from_file(config)
        cfg.CUDA = torch.cuda.is_available()
        device = torch.device("cuda" if cfg.CUDA else "cpu")

        # create model
        self.model = ModelBuilder()

        # load model
        self.model.load_state_dict(
            torch.load(snapshot, map_location=lambda storage, loc: storage.cpu())
        )
        self.model.eval().to(device)

        # build tracker
        self.tracker = build_tracker(self.model)

    def initialize(self, image_file, box):
        image = cv2.imread(image_file)
        self.tracker.init(image, box)

    def track(self, image_file):
        image = cv2.imread(image_file)
        bbox = self.tracker.track(image)["bbox"]
        return bbox
