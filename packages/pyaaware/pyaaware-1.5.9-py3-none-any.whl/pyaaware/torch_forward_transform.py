import torch


class TorchForwardTransform:
    def __init__(self,
                 N: int = 256,
                 R: int = 64,
                 bin_start: int = 1,
                 bin_end: int = 128,
                 ttype: str = 'stft-olsa-hanns') -> None:
        from pyaaware.transform_types import Overlap
        from pyaaware.transform_types import Window
        from pyaaware.transform_types import window

        self._N = N
        self._R = R
        self._bin_start = bin_start
        self._bin_end = bin_end
        self._ttype = ttype

        # Note: init is always on CPU; will move if needed in execute_all() or execute()
        self._device = 'cpu'

        if self.N % self.R:
            raise ValueError('R is not a factor of N')

        if self.bin_start >= self.N:
            raise ValueError('bin_start is greater than N')

        if self.bin_end >= self.N:
            raise ValueError('bin_end is greater than N')

        if self.bin_start >= self.bin_end:
            raise ValueError('bin_start is greater than bin_end')

        self._num_overlap = self.N // self.R
        self._overlap_indices = torch.empty((self._num_overlap, self.N), dtype=torch.int)
        for n in range(self._num_overlap):
            start = self.R * (n + 1)
            self._overlap_indices[n, :] = torch.floor(torch.tensor(range(start, start + self.N)) % self.N)

        self._bin_indices = list(range(self.bin_start, self.bin_end + 1))
        self._bins = self.bin_end - self.bin_start + 1

        self._W = None
        self._overlap_type = None
        self._xs = None
        self._overlap_count = None

        if self.ttype == 'stft-olsa-hanns':
            self._W = window(Window.NONE, self.N, self.R)
            self._W = self._W * 2 / self.N
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-ols':
            self._W = window(Window.NONE, self.N, self.R)
            self._W = self._W * 2 / self.N
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-olsa':
            self._W = window(Window.NONE, self.N, self.R)
            self._W = self._W * 2 / self.N
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-olsa-hann':
            self._W = window(Window.HANN, self.N, self.R)
            self._W = self._W * 2 / torch.sum(self._W)
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-olsa-hannd':
            self._W = window(Window.HANN, self.N, self.R)
            self._W = self._W * 2 / torch.sum(self._W)
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-olsa-hammd':
            self._W = window(Window.HAMM, self.N, self.R)
            self._W = self._W * 2 / torch.sum(self._W)
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-ola':
            self._W = window(Window.NONE, self.N, self.R)
            self._W = self._W * 2 / self.N
            self._overlap_type = Overlap.OLA
        elif self.ttype in ('tdac', 'tdac-co'):
            self._R = self.N // 2
            k = torch.arange(0, self._R + 1)
            self._W = torch.exp(-1j * 2 * torch.pi / 8 * (2 * k + 1)) * torch.exp(
                -1j * 2 * torch.pi / (2 * self.N) * k)

            if self.ttype == 'tdac':
                self._overlap_type = Overlap.TDAC
            else:
                self._overlap_type = Overlap.TDAC_CO
        else:
            raise ValueError(f"Unknown ttype: '{self.ttype}'")

        if self._overlap_type not in (Overlap.TDAC, Overlap.TDAC_CO) and len(self._W) != self.N:
            raise RuntimeError('W is not of length N')

        self.reset()

    @property
    def N(self) -> int:
        return self._N

    @property
    def R(self) -> int:
        return self._R

    @property
    def bin_start(self) -> int:
        return self._bin_start

    @property
    def bin_end(self) -> int:
        return self._bin_end

    @property
    def ttype(self) -> str:
        return self._ttype

    @property
    def device(self) -> str:
        return self._device

    @property
    def bins(self) -> int:
        return self._bins

    @property
    def W(self) -> torch.Tensor:
        return self._W

    def reset(self) -> None:
        self._xs = torch.zeros(self.N, dtype=torch.float32, device=self.device)
        self._overlap_count = 0

    def _check_device(self, xt: torch.Tensor) -> None:
        if xt.device != self.device:
            self._device = xt.device
            self._W = self.W.to(self.device)
            self._xs = self._xs.to(self.device)

    def execute_all(self, xt: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute the multichannel, forward FFT of the time domain input.

        :param xt: Tensor of time domain data with dimensions [batch, samples]
        :return: Tuple containing frequency domain frame data and frame-based energy data
            yf: [batch, frames, bins]
            energy_t: [batch, frames]
        """
        import numpy as np

        if xt.ndim != 1 and xt.ndim != 2:
            raise ValueError('Input must have 1 or 2 dimensions')

        self._check_device(xt)

        no_batch = xt.ndim == 1
        if no_batch:
            batches = 1
            samples = xt.shape[0]
        else:
            batches, samples = xt.shape

        frames = int(np.ceil(samples / self.R))
        extra_samples = frames * self.R - samples
        if no_batch:
            pad = (0, extra_samples)
        else:
            pad = (0, 0, 0, extra_samples)

        xt_pad = torch.nn.functional.pad(input=xt,
                                         pad=pad,
                                         mode='constant',
                                         value=0)
        if no_batch:
            yf = torch.empty((frames, self.bins), dtype=torch.complex64)
            energy_t = torch.empty(frames, dtype=torch.float32)
        else:
            yf = torch.empty((batches, frames, self.bins), dtype=torch.complex64)
            energy_t = torch.empty((batches, frames), dtype=torch.float32)

        for batch in range(batches):
            for frame in range(frames):
                start = frame * self.R
                stop = start + self.R
                if no_batch:
                    yf[frame, :], energy_t[frame] = self.execute(xt_pad[start:stop])
                else:
                    yf[batch, frame, :], energy_t[batch, frame] = self.execute(xt_pad[batch, start:stop])
            self.reset()

        return yf, energy_t

    def execute(self, xt: torch.Tensor) -> tuple[torch.Tensor, float]:
        """Compute the forward FFT of the time domain input.

        :param xt: Tensor of time domain data with dimensions [samples]
        :return: Tuple containing frequency domain frame data and frame-based energy data
            yf: [bins]
            energy_t: scalar
        """
        import numpy as np

        from pyaaware.transform_types import Overlap

        if xt.ndim != 1:
            raise ValueError('Input must have 1 dimensions [bins]')

        if xt.shape[0] != self.R:
            raise ValueError(f'Input must have {self.R} samples')

        self._check_device(xt)

        if self._overlap_type == Overlap.OLA:
            ytn = self.W * torch.concatenate((xt, torch.zeros(self.N - self.R,
                                                              dtype=torch.float32,
                                                              device=self.device)))
            energy_t = torch.mean(torch.square(xt))
            tmp = torch.fft.rfft(ytn)
        elif self._overlap_type == Overlap.OLS:
            self._xs[self._overlap_indices[self._overlap_count, (self.N - self.R):self.N]] = xt
            ytn = self._xs[self._overlap_indices[self._overlap_count, :]]
            energy_t = torch.mean(torch.square(ytn))
            ytn = self.W * ytn
            tmp = torch.fft.rfft(ytn)
            self._overlap_count = (self._overlap_count + 1) % self._num_overlap
        elif self._overlap_type in (Overlap.TDAC, Overlap.TDAC_CO):
            self._xs[self._overlap_indices[self._overlap_count, (self.N - self.R):self.N]] = xt
            ytn = self._xs[self._overlap_indices[self._overlap_count, :]]
            energy_t = torch.mean(torch.square(ytn))
            tmp = np.sqrt(1 / self.N) * torch.fft.rfft(ytn)
            tmp = 1j * self.W[0:self.R] * tmp[0:self.R] + self.W[1:self.R + 1] * tmp[1:self.R + 1]
            if self._overlap_type == Overlap.TDAC_CO:
                tmp = torch.real(tmp)
            self._overlap_count = (self._overlap_count + 1) % self._num_overlap
        else:
            raise ValueError(f"Unsupported overlap type: '{self._overlap_type}")

        yf = tmp[self._bin_indices]
        return yf, float(energy_t)
