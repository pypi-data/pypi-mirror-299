import pytest
import torch as th

from torchlure.functions import iqm


def test_iqm_basic_case():
    """Test basic case for 1D tensor with keepdim=True"""
    x = th.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
    expected = th.tensor([3.0])
    result = iqm(x, keepdim=True)
    assert th.allclose(result, expected), f"Expected {expected}, but got {result}"


def test_iqm_basic_case_no_keepdim():
    """Test basic case for 1D tensor with keepdim=False"""
    x = th.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
    expected = th.tensor(3.0)
    result = iqm(x, keepdim=False)
    assert th.allclose(result, expected), f"Expected {expected}, but got {result}"


def test_iqm_with_nan_values():
    """Test IQM calculation with NaN values"""
    x = th.tensor([1.0, 2.0, float("nan"), 4.0, 5.0])
    expected = th.tensor([3.0])
    result = iqm(x, keepdim=True)
    assert th.allclose(result, expected, equal_nan=True), f"Expected {expected}, but got {result}"


def test_iqm_multidimensional_tensor_dim_0():
    """Test IQM calculation for multi-dimensional tensor along dimension 0"""
    x = th.tensor(
        [
            [1.0, 2.0, 3.0, 4.0, 5.0],
            [2.0, 3.0, 4.0, 5.0, 6.0],
            [3.0, 4.0, 5.0, 6.0, 7.0],
            [4.0, 5.0, 6.0, 7.0, 8.0],
            [5.0, 6.0, 7.0, 8.0, 9.0],
            [6.0, 7.0, 8.0, 9.0, 10.0],
            [7.0, 8.0, 9.0, 10.0, 11.0],
            [8.0, 9.0, 10.0, 11.0, 12.0],
        ],
    )

    expected = th.tensor([4.5, 5.5, 6.5, 7.5, 8.5])

    result = iqm(x, dim=0, keepdim=False)
    assert th.allclose(result, expected, atol=1e-6), f"Expected {expected}, but got {result}"


def test_iqm_multidimensional_tensor_dim_1():
    """Test IQM calculation for multi-dimensional tensor along dimension 1"""
    x = th.tensor([[1.0, 2.0, 3.0, 4.0, 5.0], [2.0, 3.0, 4.0, 5.0, 6.0]])
    expected = th.tensor([[3.0], [4.0]])
    result = iqm(x, dim=1, keepdim=True)
    assert th.allclose(result, expected), f"Expected {expected}, but got {result}"


def test_iqm_multidimensional_tensor_dim_1_no_keepdim():
    """Test IQM calculation for multi-dimensional tensor along dimension 1 with keepdim=False"""
    x = th.tensor([[1.0, 2.0, 3.0, 4.0, 5.0], [2.0, 3.0, 4.0, 5.0, 6.0]])
    expected = th.tensor([3.0, 4.0])
    result = iqm(x, dim=1, keepdim=False)
    assert th.allclose(result, expected), f"Expected {expected}, but got {result}"


def test_iqm_flatten_case():
    """Test IQM calculation for tensor with no dimension specified (flattened case)"""
    x = th.tensor([[1.0, 2.0], [3.0, 4.0]])
    expected = th.tensor(2.5)
    result = iqm(x)
    assert th.allclose(result, expected), f"Expected {expected}, but got {result}"


def test_iqm_large_input_tensor():
    """Test IQM calculation for a large input tensor"""
    x = th.arange(1000.0).reshape(10, 100)
    expected = th.tensor([49.5, 149.5, 249.5, 349.5, 449.5, 549.5, 649.5, 749.5, 849.5, 949.5])
    result = iqm(x, dim=1)
    assert th.allclose(result, expected), f"Expected {expected}, but got {result}"


def test_iqm_gpu_support():
    """Test IQM calculation on GPU"""
    if th.cuda.is_available():
        x = th.tensor([1.0, 2.0, 3.0, 4.0, 5.0], device="cuda")
        expected = th.tensor([3.0], device="cuda")
        result = iqm(x, keepdim=True)
        assert th.allclose(result, expected), f"Expected {expected.cpu()}, but got {result.cpu()}"
