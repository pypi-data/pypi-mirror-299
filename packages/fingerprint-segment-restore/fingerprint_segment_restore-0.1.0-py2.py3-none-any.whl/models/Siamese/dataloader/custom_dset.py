from .base_dset import BaseDset

from pathlib import Path
import sys
root_path = Path(__file__).parents[3].as_posix()
sys.path.append(root_path)
from src.dl_matcher.siamese.config.base_config import cfg



class Custom(BaseDset):

    def __init__(self, yaml_cfg):
        super(Custom, self).__init__(yaml_cfg)

    def load(self):
        base_path = self.yaml_cfg.DATASETS.CUSTOM.HOME
        super(Custom, self).load(base_path)
