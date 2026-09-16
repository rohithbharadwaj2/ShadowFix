# ShadowFix Experiments

This page summarizes the experiment workflow documented in the original project README, Colab export, final report, and presentation.

## Problem

ShadowFix studies supervised removal of cast shadows from real-world images. ISTD triplets provide a shadowed RGB image, a binary shadow mask, and a shadow-free target.

## Compared Approaches

1. **RGB U-Net baseline** — RGB input only.
2. **RGB Residual U-Net** — RGB-only restoration using a residual output formulation.
3. **Mask-Guided U-Net** — RGB image plus shadow-mask information.
4. **Traditional correction** — non-neural comparison method included in evaluation.

## Data

The documented split contains:

- 1,197 training triplets
- 133 validation triplets
- 540 held-out test triplets

Reported neural experiments resize images to 256 × 256.

## Recorded Training Commands

The original Colab workflow records a baseline experiment with:

```text
image size       256
batch size       8
epochs           50
learning rate    2e-4
base channels    32
shadow weight    1
nonshadow weight 1
AMP               enabled
```

The mask-guided experiment records:

```text
image size       256
batch size       8
epochs           50
learning rate    2e-4
base channels    32
mask input       enabled
shadow weight    4
nonshadow weight 1
edge weight      0.05
AMP               enabled
```

A later RGB experiment in the Colab export uses a residual output mode with learning rate `1e-4`, shadow weight `6`, non-shadow weight `1`, and edge weight `0.10`.

## Final Quantitative Comparison

| Model | PSNR (dB) | SSIM | Shadow PSNR | Non-Shadow PSNR |
|---|---:|---:|---:|---:|
| **Mask-Guided U-Net** | **30.189** | **0.9514** | **26.303** | **31.887** |
| RGB U-Net baseline | 27.176 | 0.9324 | 24.097 | 28.549 |
| RGB Residual U-Net (50 epochs) | 26.589 | 0.9268 | 25.062 | 27.223 |
| RGB Residual U-Net (continued) | 26.428 | 0.9268 | 25.027 | 27.036 |

The original README additionally records the traditional correction comparison at **24.700 dB PSNR**.

## Benchmark vs. Interactive Demo

The best benchmark model and the automatic demo model serve different constraints:

- **Mask-Guided U-Net** gives the strongest quantitative benchmark but requires mask information.
- **RGB Residual U-Net (`baseline_final/best.pth`)** was selected for the automatic Gradio demo because arbitrary RGB images can be processed without a ground-truth mask.

The Gradio workflow also includes a guided mode where a user paints an approximate shadow region and controls restoration strength.

## Important Reproducibility Note

The materials currently available for this public repository include the final Colab workflow/export and project documentation, but not the original `shadow_removal_project/` source directory or model checkpoint binaries referenced by that workflow. The repository therefore does **not** claim that full training/inference can currently be reproduced from this public snapshot alone.

Rather than reconstructing undocumented source code, this repository preserves verified experiment settings, results, and authentic demo utilities from the available materials. If the original project source/checkpoints are recovered later, they can be added without changing the reported results.
