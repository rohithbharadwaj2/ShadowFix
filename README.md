# ShadowFix

## Deep Learning for Real-World Shadow Removal

ShadowFix is a computer-vision image-restoration project comparing RGB, residual, and mask-guided U-Net approaches for removing real-world shadows while preserving non-shadow content.

> **Best reported benchmark:** **30.189 dB PSNR · 0.9514 SSIM · 26.303 dB Shadow-Region PSNR** on **540 held-out ISTD test triplets**.

**Python · PyTorch · OpenCV · U-Net · Gradio · NumPy · CUDA**

---

## Highlights

- Compared **RGB U-Net**, **RGB Residual U-Net**, **Mask-Guided U-Net**, and traditional shadow correction.
- Evaluated overall **PSNR / SSIM** plus **shadow- and non-shadow-region PSNR**.
- Mask guidance improved overall PSNR by **+3.01 dB** and shadow-region PSNR by **+2.21 dB** over the RGB baseline.
- Built automatic and guided Gradio workflows for real-world testing.
- Documented out-of-distribution behavior, mask sensitivity, visible boundary artifacts, and limitations rather than reporting benchmark metrics alone.

## Results

| Model | PSNR (dB) | SSIM | Shadow PSNR | Non-Shadow PSNR |
|---|---:|---:|---:|---:|
| **Mask-Guided U-Net** | **30.189** | **0.9514** | **26.303** | **31.887** |
| RGB U-Net baseline | 27.176 | 0.9324 | 24.097 | 28.549 |
| RGB Residual U-Net (50 epochs) | 26.589 | 0.9268 | 25.062 | 27.223 |
| RGB Residual U-Net (continued) | 26.428 | 0.9268 | 25.027 | 27.036 |

The project README also records traditional correction at **24.700 dB PSNR**.

### Why mask guidance helped

The mask-guided model receives explicit information about where the shadow lies. In the reported experiments this produced the strongest result across all four quantitative metrics, allowing restoration to focus on affected pixels while better preserving surrounding content.

---

## Experimental Pipeline

```text
ISTD Dataset
Shadow Image + Shadow Mask + Shadow-Free Target
                     │
                     ▼
              Data Preparation
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
      RGB Models         Mask-Guided Model
          │                     │
          └──────────┬──────────┘
                     ▼
                  Training
                     │
                     ▼
                 Evaluation
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      PSNR          SSIM      Region PSNR
                     │
                     ▼
               Gradio Prototype
              ┌──────┴──────┐
              ▼             ▼
          Automatic       Guided
             Mode          Mode
```

## Dataset

Experiments use the **ISTD (Image Shadow Triplets Dataset)**. Each sample contains a shadow image, binary shadow mask, and shadow-free ground truth.

| Split | Samples |
|---|---:|
| Training | 1,197 |
| Validation | 133 |
| Test | 540 |

Reported neural experiments resize images to **256 × 256**. ISTD is not redistributed here.

## Recorded Training Setup

The original Colab workflow records the following primary settings:

| Parameter | RGB baseline | Mask-guided |
|---|---:|---:|
| Image size | 256 | 256 |
| Batch size | 8 | 8 |
| Epochs | 50 | 50 |
| Learning rate | 2e-4 | 2e-4 |
| Base channels | 32 | 32 |
| Shadow weight | 1 | 4 |
| Non-shadow weight | 1 | 1 |
| Edge weight | — | 0.05 |
| AMP | enabled | enabled |

A later RGB residual experiment recorded in the Colab export uses learning rate `1e-4`, shadow weight `6`, non-shadow weight `1`, edge weight `0.10`, and residual output mode.

For more detail, see [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md).

---

## Interactive Demo

The submitted Gradio prototype contains two workflows.

### Automatic Mode

The automatic demo uses the **RGB Residual U-Net checkpoint (`baseline_final/best.pth`)** because it can process an arbitrary RGB image without requiring a ground-truth mask.

### Guided Mode

The user can paint an approximate shadow region and control restoration strength. The original workflow also includes a local-luminance shadow-mask heuristic and mask-aware blending logic; the reusable parts available in the submitted Colab export are preserved in [`app/demo_utils.py`](app/demo_utils.py).

> **Benchmark vs. demo:** the Mask-Guided U-Net is the best reported benchmark model, but it requires mask information. The automatic demo intentionally uses an RGB model for practical user input.

---

## Evaluation

**PSNR** measures pixel-level reconstruction similarity to the shadow-free target.

**SSIM** measures structural similarity in luminance, contrast, and local structure.

**Shadow-region PSNR** evaluates correction specifically inside the shadow mask.

**Non-shadow-region PSNR** evaluates preservation of areas that should remain unchanged.

Using region-specific metrics matters because aggressive brightening can improve the shadow while damaging unaffected content.

---

## Limitations

- 256 × 256 training can lose fine high-resolution detail.
- Mask-guided restoration depends strongly on mask quality.
- External phone/internet images can differ substantially from ISTD.
- Difficult cases can retain faint boundaries, color shifts, or smoothed texture.
- PSNR and SSIM do not fully represent perceptual realism; LPIPS and human evaluation are reasonable future additions.

## Public Repository Scope

The materials available for this public cleanup include the **final Colab workflow/export, final report, presentation, project README, and recorded demo**. The original submission documentation references a separate `shadow_removal_project/` directory containing `train.py`, `evaluate.py`, dataset handling, inference code, and utilities, plus `.pth` checkpoints. Those source/checkpoint files are **not present in the materials currently available here**.

For that reason, this repository deliberately does **not** invent replacement training/inference code or claim that the complete experiment is reproducible from this snapshot. It preserves the verified results, recorded configurations, experiment documentation, and authentic demo utilities that are supported by the available project materials.

---

## Repository Structure

```text
ShadowFix/
├── app/
│   └── demo_utils.py            # Utilities extracted from original Gradio workflow
├── configs/
│   ├── rgb_baseline.yaml        # Recorded baseline configuration
│   └── mask_guided.yaml         # Recorded mask-guided configuration
├── docs/
│   ├── EXPERIMENTS.md           # Experiment and reproducibility notes
│   └── README.md                # Documentation index
├── results/
│   └── model_comparison.csv     # Final reported benchmark table
├── assets/
│   └── README.md                # Visual-asset placement guide
├── .gitignore
├── requirements.txt
└── README.md
```

## Team & Contributions

This project was developed collaboratively by **Odra Bira, Pranay Lachuluri, and Rohith Bharadwaj**.

**Rohith Bharadwaj's documented contributions:** evaluation design, model-comparison analysis, Gradio interface testing, qualitative result selection, failure-case analysis, and documentation review. All team members participated in reviewing results, discussing failure cases, and preparing the final presentation narrative.

## Future Work

- Recover and publish the original training/evaluation source if available and permitted.
- Integrate learned shadow detection with restoration for a fully automatic pipeline.
- Evaluate perceptual quality with LPIPS and human preference studies.
- Explore higher-resolution and multi-scale restoration.
- Improve robustness to out-of-distribution lighting, cameras, and surfaces.

## License

No open-source license is asserted yet. Before redistributing or reusing project code, model checkpoints, dataset content, or third-party assets, verify the applicable permissions and ISTD terms.
