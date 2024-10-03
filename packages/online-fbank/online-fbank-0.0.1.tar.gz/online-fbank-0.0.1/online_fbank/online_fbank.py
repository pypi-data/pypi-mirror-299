# Copyright (c) 2024, Zhendong Peng (pzd17@tsinghua.org.cn)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import kaldi_native_fbank as knf
import numpy as np


class OnlineFbank(knf.OnlineFbank):
    def __init__(self, sample_rate=16000, window_type="povey", dither=0, num_bins=80):
        opts = knf.FbankOptions()
        opts.frame_opts.dither = dither
        opts.frame_opts.samp_freq = sample_rate
        opts.frame_opts.snip_edges = False
        opts.frame_opts.window_type = window_type
        opts.mel_opts.debug_mel = False
        opts.mel_opts.num_bins = num_bins
        super().__init__(opts)

        self.sample_rate = sample_rate

    def accept_waveform(self, samples, is_last=False):
        super().accept_waveform(self.sample_rate, samples)
        if is_last:
            super().input_finished()

    def get_frames(self, num_frames=None):
        num_frames = num_frames or self.num_frames_ready
        frames = []
        for i in range(num_frames):
            frames.append(super().get_frame(i))
        return np.stack(frames) if len(frames) > 0 else None

    def get_lfr_frames(self, window_size=7, window_shift=6, neg_mean=0, inv_stddev=1):
        num_lfr_frames = (self.num_frames_ready - window_size) // window_shift
        if num_lfr_frames <= 0:
            return None

        num_frames = window_size + num_lfr_frames * window_shift
        is_last_frame = super().is_last_frame(num_frames)
        frames = self.get_frames(num_frames if not is_last_frame else None)
        lfr_frames = np.lib.stride_tricks.as_strided(
            frames,
            shape=(num_lfr_frames, frames.shape[1] * window_size),
            strides=((window_shift * frames.shape[1]) * 4, 4),
        )
        return (lfr_frames + neg_mean) * inv_stddev
