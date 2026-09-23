"""
BhashaAI — CUDA / Hardware Diagnostic Tests
Checks PyTorch CUDA availability, device details, and VRAM.
"""

import unittest
import torch
from src.config import get_device


class TestCUDA(unittest.TestCase):

    def test_cuda_availability(self):
        """Check if CUDA is available and display device info."""
        device = get_device()
        self.assertIn(device.type, ["cuda", "cpu"])
        print(f"\n[Hardware Diagnostic] Active PyTorch Device: {device}")

        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0)
            total_memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"[Hardware Diagnostic] CUDA Device Count: {device_count}")
            print(f"[Hardware Diagnostic] GPU 0: {device_name}")
            print(f"[Hardware Diagnostic] VRAM: {total_memory_gb:.2f} GB")
            self.assertGreater(device_count, 0)
        else:
            print("[Hardware Diagnostic] Running on CPU (CUDA not available or PyTorch CPU edition installed).")


if __name__ == "__main__":
    unittest.main()
