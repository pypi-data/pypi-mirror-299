import pytest
import torch as th

from torchlure import iqm


def test_iqm_basic_case():
    x = th.tensor([[1.0, 2.0, 3.0, 4.0, 5.0]])
    expected = th.tensor([[3.0]])
    result = iqm(x, keepdim=True)
    assert th.allclose(result, expected), f"Expected {expected}, but got {result}"


def test_iqm_basic_case_no_keepdim():
    x = th.tensor([[1.0, 2.0, 3.0, 4.0, 5.0]])
    expected = th.tensor([3.0])
    result = iqm(x, keepdim=False)
    assert th.allclose(result, expected), f"Expected {expected}, but got {result}"


def test_iqm_with_nan_values():
    x = th.tensor([[1.0, 2.0, th.nan, 4.0, 5.0]])
    expected = th.tensor([[3.0]])
    result = iqm(x, keepdim=True)
    assert th.allclose(result, expected, equal_nan=True), f"Expected {expected}, but got {result}"


def test_iqm_multidimensional_tensor():
    x = th.tensor([[[1.0, 2.0, 3.0, 4.0, 5.0], [2.0, 3.0, 4.0, 5.0, 6.0]]])
    expected = th.tensor([[[3.0], [4.0]]])
    result = iqm(x, keepdim=True)
    assert th.allclose(result, expected), f"Expected {expected}, but got {result}"


def test_iqm_gpu_support():
    if th.cuda.is_available():
        x = th.tensor([[1.0, 2.0, 3.0, 4.0, 5.0]], device="cuda")
        expected = th.tensor([[3.0]], device="cuda")
        result = iqm(x, keepdim=True)
        assert th.allclose(result, expected), f"Expected {expected.cpu()}, but got {result.cpu()}"
