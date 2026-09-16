"""Utilities extracted from the original ShadowFix Colab/Gradio workflow.

These functions preserve the automatic shadow-mask heuristic and guided
restoration blending logic used by the submitted demo while removing
Google Colab and Google Drive path dependencies.
"""

from __future__ import annotations

import cv2
import numpy as np
from PIL import Image


def pil_rgb(image) -> Image.Image | None:
    """Normalize a PIL image, numpy array, or image path to RGB PIL."""
    if image is None:
        return None
    if isinstance(image, Image.Image):
        return image.convert("RGB")
    if isinstance(image, np.ndarray):
        if image.ndim == 2:
            return Image.fromarray(image.astype(np.uint8)).convert("RGB")
        if image.shape[-1] == 4:
            image = image[:, :, :3]
        return Image.fromarray(image.astype(np.uint8)).convert("RGB")
    return Image.open(image).convert("RGB")


def automatic_shadow_mask(image) -> Image.Image:
    """Estimate a coarse shadow mask using local LAB luminance contrast.

    This is the heuristic used in the original Gradio workflow. It is not
    the ground-truth ISTD mask and is intentionally described as a demo
    aid rather than a learned shadow detector.
    """
    image = pil_rgb(image)
    if image is None:
        raise ValueError("An input image is required.")

    rgb = np.array(image)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    luminance = lab[:, :, 0].astype(np.float32)

    local_mean = cv2.GaussianBlur(luminance, (0, 0), sigmaX=35, sigmaY=35)
    darkness = local_mean - luminance
    mask = (darkness > 10).astype(np.uint8) * 255

    small_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, small_kernel)

    large_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, large_kernel)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    clean_mask = np.zeros_like(mask)
    min_area = 1500

    for component in range(1, num_labels):
        area = stats[component, cv2.CC_STAT_AREA]
        if area >= min_area:
            clean_mask[labels == component] = 255

    return Image.fromarray(clean_mask, mode="L")


def blend_restoration(
    original: Image.Image,
    restored: Image.Image,
    mask: Image.Image,
    strength: float = 1.0,
    feather_sigma: float = 7.0,
) -> Image.Image:
    """Blend a restored image into user-selected shadow regions.

    The helper captures the guided-demo behavior without depending on the
    unavailable training project directory or checkpoint files.
    """
    original = pil_rgb(original)
    restored = pil_rgb(restored)
    if original is None or restored is None:
        raise ValueError("Both original and restored images are required.")

    restored = restored.resize(original.size, Image.Resampling.BILINEAR)
    mask = mask.convert("L").resize(original.size, Image.Resampling.BILINEAR)

    src = np.asarray(original, dtype=np.float32)
    pred = np.asarray(restored, dtype=np.float32)
    alpha = np.asarray(mask, dtype=np.float32) / 255.0

    if feather_sigma > 0:
        alpha = cv2.GaussianBlur(alpha, (0, 0), sigmaX=feather_sigma, sigmaY=feather_sigma)

    alpha = np.clip(alpha * float(strength), 0.0, 1.0)[..., None]
    output = src * (1.0 - alpha) + pred * alpha
    return Image.fromarray(np.clip(output, 0, 255).astype(np.uint8))
