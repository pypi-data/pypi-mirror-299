import os
from typing import Callable, List

import numpy as np

from physioex.data.base import PhysioExDataset
from physioex.data.constant import get_data_folder

AVAILABLE_PICKS = ["EEG", "EOG", "EMG"]


class Dreem(PhysioExDataset):
    def __init__(
        self,
        version: str = "dodh",  # available ["dodo", dodh]
        picks: List[str] = ["EEG"],  # available [ "EEG", "EOG", "EMG", "ECG" ]
        preprocessing: str = "raw",  # available [ "raw", "xsleepnet" ]
        sequence_length: int = 21,
        target_transform: Callable = None,
        task: str = "sleep",
    ):
        assert version in ["dodo", "dodh"], "version should be one of 'dodo'-'dodh'"

        assert preprocessing in [
            "raw",
            "xsleepnet",
        ], "preprocessing should be one of 'raw'-'xsleepnet'"
        for pick in picks:
            assert pick in AVAILABLE_PICKS, "pick should be one of 'EEG, 'EOG', 'EMG'"

        selected_channels = np.array(
            [AVAILABLE_PICKS.index(pick) for pick in picks]
        ).astype(int)

        input_shape = [3, 3000] if preprocessing == "raw" else [3, 29, 129]

        super().__init__(
            dataset_folder=os.path.join(get_data_folder(), "dreem", version),
            preprocessing=preprocessing,
            input_shape=input_shape,
            sequence_length=sequence_length,
            selected_channels=selected_channels,
            target_transform=target_transform,
        )

    def __getitem__(self, idx):
        x, y = super().__getitem__(idx)

        x = (x - self.mean) / self.std

        if self.target_transform is not None:
            y = self.target_transform(y)

        return x, y
