import torch

from src.models import build_model


def test_rgb_model_output_shape_and_range():
    model = build_model(mask_guided=False, base_channels=8).eval()
    x = torch.rand(1, 3, 64, 64)
    with torch.no_grad():
        y = model(x)
    assert y.shape == (1, 3, 64, 64)
    assert torch.all(y >= 0) and torch.all(y <= 1)


def test_mask_guided_model_accepts_four_channels():
    model = build_model(mask_guided=True, base_channels=8).eval()
    x = torch.rand(1, 4, 64, 64)
    with torch.no_grad():
        y = model(x)
    assert y.shape == (1, 3, 64, 64)
