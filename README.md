# ShadowFix

## Deep Learning for Real-World Shadow Removal

ShadowFix is a computer-vision image-restoration project studying how U-Net formulations remove real-world shadows while preserving texture, color, and non-shadow regions.

The project evaluates RGB, residual, and mask-guided restoration approaches on the ISTD benchmark and includes quantitative evaluation, region-specific analysis, failure-case analysis, and an interactive Gradio prototype.

> **Best benchmark result:** **30.189 dB PSNR · 0.9514 SSIM · 26.303 dB Shadow-Region PSNR** on 540 held-out ISTD test triplets.

**Tech:** Python · PyTorch · OpenCV · U-Net · Gradio · NumPy · CUDA

---

## Highlights

- Compared four restoration variants under a common evaluation pipeline.
- Evaluated overall PSNR/SSIM as well as shadow- and non-shadow-region PSNR.
- Mask guidance improved overall PSNR by **+3.01 dB** and shadow-region PSNR by **+2.21 dB** over the RGB baseline.
- Built automatic and guided Gradio workflows for testing restoration on real-world images.
- Analyzed out-of-distribution behavior, mask sensitivity, and restoration artifacts rather than reporting benchmark metrics alone.

## Results

| Model | PSNR (dB) | SSIM | Shadow PSNR | Non-Shadow PSNR |
|---|---:|---:|---:|---:|
| **Mask-Guided U-Net** | **30.189** | **0.9514** | **26.303** | **31.887** |
| RGB Baseline | 27.176 | 0.9324 | 24.097 | 28.549 |
| RGB Residual (50 epochs) | 26.589 | 0.9268 | 25.062 | 27.223 |
| RGB Residual (continued) | 26.428 | 0.9268 | 25.027 | 27.036 |

### What the results show

The mask-guided model produced the strongest result across every reported metric. Explicit shadow-location information lets the network focus restoration on the affected region while better preserving surrounding content.

The residual variants corrected shadow regions more strongly than the RGB baseline in some cases, but changed non-shadow regions more aggressively, reducing overall benchmark performance. This trade-off is useful because visually stronger correction does not necessarily correspond to better full-image reconstruction metrics.

---

## System Overview

```text
ISTD Triplets
Shadow Image + Mask + Shadow-Free Target
                 │
                 ▼
          Data Preparation
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
   RGB Models       Mask-Guided U-Net
       │                   │
       └─────────┬─────────┘
                 ▼
              Training
                 │
                 ▼
             Evaluation
       ┌─────────┼──────────┐
       ▼         ▼          ▼
     PSNR       SSIM    Region PSNR
                 │
                 ▼
           Gradio Prototype
          ┌──────┴──────┐
          ▼             ▼
      Automatic       Guided
        Mode           Mode
```

## Model Variants

### RGB Baseline
A three-channel shadow image is mapped directly to a three-channel restored image. This is the simplest automatic setting because no shadow mask is required.

### Mask-Guided U-Net
The model receives the RGB image together with a shadow mask. The mask tells the network where restoration is needed, reducing the burden of simultaneously localizing and correcting the shadow.

```text
RGB Image + Shadow Mask → U-Net → Restored RGB Image
```

This model achieved the strongest benchmark performance.

### RGB Residual Variants
The residual formulation predicts a correction to the input rather than reconstructing the complete output from scratch. It preserved useful source texture but could alter non-shadow regions more aggressively.

---

## Dataset

Experiments use the **ISTD (Image Shadow Triplets Dataset)**. Each sample contains a shadow image, binary shadow mask, and corresponding shadow-free target.

| Split | Samples |
|---|---:|
| Training | 1,197 |
| Validation | 133 |
| Test | 540 |

Images were resized to **256 × 256** for the reported experiments. The dataset itself is **not redistributed in this repository**; obtain it from its official source and follow its licensing terms.

## Training Configuration

| Parameter | Value |
|---|---|
| Image size | 256 × 256 |
| Batch size | 8 |
| Base channels | 32 |
| Framework | PyTorch |
| Training hardware | NVIDIA Tesla T4 |
| Precision | Automatic Mixed Precision |

Mask-guided training used stronger weighting inside the shadow region so that the objective prioritizes the area requiring correction while still penalizing unwanted changes elsewhere.

---

## Evaluation

**PSNR** measures pixel-level reconstruction similarity to the shadow-free target.

**SSIM** measures structural similarity using local luminance, contrast, and structure.

**Shadow-region PSNR** isolates reconstruction quality inside the shadow mask.

**Non-shadow-region PSNR** measures how well the model preserves content that should remain unchanged.

Region-specific evaluation is important: a model can brighten a shadow aggressively while damaging unaffected parts of the image, or achieve a strong global metric while leaving visible shadow artifacts.

---

## Interactive Demo

ShadowFix includes two prototype workflows.

### Automatic Mode
Users provide an RGB image and receive a restored output without supplying a ground-truth mask. The automatic prototype uses an RGB model because it can operate directly on arbitrary RGB input.

### Guided Mode
Users paint an approximate shadow region and select restoration strength. The generated mask controls where the restored result is blended into the source image.

> **Benchmark vs. demo:** the Mask-Guided U-Net is the strongest benchmark model but requires a shadow mask. The automatic demo therefore uses an RGB model so users can test arbitrary images without ground-truth mask information.

---

## Limitations

- Training at 256 × 256 can lose fine high-resolution texture.
- Mask-guided restoration depends on mask quality.
- Phone/internet images may differ substantially from the ISTD training distribution.
- Difficult examples can retain faint boundaries, color shifts, or over-smoothed texture.
- PSNR and SSIM do not completely measure perceptual realism; perceptual metrics such as LPIPS and user studies would be useful extensions.

## Future Work

- Integrate learned shadow detection with restoration for a fully automatic pipeline.
- Evaluate perceptual quality with LPIPS and human preference studies.
- Explore higher-resolution and multi-scale restoration.
- Improve robustness to out-of-distribution lighting, cameras, and surfaces.

---

## Repository Structure

```text
ShadowFix/
├── src/                  # Reusable model, data, training and evaluation modules
├── app/                  # Gradio application
├── configs/              # Reproducible experiment configurations
├── results/              # Benchmark results
├── tests/                # Lightweight validation tests
├── docs/                 # Project documentation
├── assets/               # Demo and README visuals
├── requirements.txt
└── README.md
```

## Team & Contributions

This project was developed collaboratively by **Odra Bira, Pranay Lachuluri, and Rohith Bharadwaj**.

**Rohith Bharadwaj's documented contributions:** evaluation design, model-comparison analysis, Gradio interface testing, qualitative result selection, failure-case analysis, and documentation review. All team members participated in reviewing outputs, discussing failure cases, and preparing the final presentation narrative.

## Reproducibility

Experiment configurations and benchmark results are versioned in this repository. Dataset files and large model checkpoints are intentionally excluded from normal Git history.

## License

No open-source license is asserted yet. Before redistributing or reusing project code, models, or third-party assets, verify the applicable permissions and dataset terms.
