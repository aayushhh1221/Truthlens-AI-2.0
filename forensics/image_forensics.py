"""
TruthLens AI 2.0 — Image Forensics Engine
Real signal-based image analysis: ELA, EXIF, noise, compression, edge analysis.
"""
import io
import math
import struct
from PIL import Image, ImageChops, ImageFilter, ImageStat
import numpy as np

from utils.config import ELA_QUALITY, ELA_SCALE


# ─── ELA (Error Level Analysis) ──────────────────────────────

def run_ela(image_bytes: bytes) -> dict:
    """
    Perform Error Level Analysis.
    Re-saves image at a known quality and amplifies differences.
    High ELA variance in uniform regions → manipulation suspected.
    """
    try:
        original = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Re-save at controlled quality
        buffer = io.BytesIO()
        original.save(buffer, "JPEG", quality=ELA_QUALITY)
        buffer.seek(0)
        recompressed = Image.open(buffer).convert("RGB")

        # Compute absolute difference
        diff = ImageChops.difference(original, recompressed)

        # Scale up for visibility
        extrema = diff.getextrema()
        max_diff = max(e[1] for e in extrema) if extrema else 1
        if max_diff == 0:
            max_diff = 1
        scale = 255.0 / max_diff * ELA_SCALE
        diff_scaled = diff.point(lambda p: min(int(p * scale), 255))

        stat = ImageStat.Stat(diff_scaled)
        mean_ela   = float(np.mean(stat.mean))
        std_ela    = float(np.mean(stat.stddev))

        # High mean ELA on re-saved image = lower quality original or manipulation
        manipulation_score = min(int(mean_ela / 255 * 200), 100)

        return {
            "mean_ela":          round(mean_ela, 2),
            "std_ela":           round(std_ela, 2),
            "manipulation_score": manipulation_score,
            "findings": _ela_findings(mean_ela, std_ela),
        }
    except Exception as e:
        return {"mean_ela": 0, "std_ela": 0, "manipulation_score": 0,
                "findings": [f"ELA error: {str(e)}"]}


def _ela_findings(mean: float, std: float) -> list:
    findings = []
    if mean > 30:
        findings.append(f"Elevated ELA mean ({mean:.1f}) — possible manipulation")
    elif mean > 15:
        findings.append(f"Moderate ELA levels ({mean:.1f}) — minor edits possible")
    else:
        findings.append(f"Low ELA levels ({mean:.1f}) — consistent with original")

    if std > 20:
        findings.append("High ELA variance — uneven compression suggests splicing")
    return findings


# ─── EXIF Metadata Analysis ───────────────────────────────────

def run_exif_analysis(image_bytes: bytes) -> dict:
    """Extract and analyze EXIF metadata for anomalies."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        exif_data = img._getexif() if hasattr(img, "_getexif") else None

        if not exif_data:
            return {
                "has_exif": False,
                "flags": ["No EXIF metadata found — common in screenshots or stripped originals"],
                "metadata": {},
                "anomaly_score": 20,
            }

        # EXIF tag IDs we care about
        TAG_MAP = {
            271: "Make", 272: "Model", 305: "Software",
            306: "DateTime", 36867: "DateTimeOriginal",
            36868: "DateTimeDigitized", 40961: "ColorSpace",
            33434: "ExposureTime", 33437: "FNumber",
            34855: "ISO", 37386: "FocalLength",
            40962: "PixelXDimension", 40963: "PixelYDimension",
        }

        metadata = {}
        for tag_id, name in TAG_MAP.items():
            if tag_id in exif_data:
                val = exif_data[tag_id]
                metadata[name] = str(val)

        flags  = []
        score  = 0

        # Check software field (editing software)
        software = metadata.get("Software", "").lower()
        editing_sw = ["photoshop", "gimp", "lightroom", "affinity", "pixelmator", "canva"]
        if any(sw in software for sw in editing_sw):
            flags.append(f"Editing software detected: {metadata['Software']}")
            score += 35

        # Date consistency
        dt_orig  = metadata.get("DateTimeOriginal", "")
        dt_digit = metadata.get("DateTimeDigitized", "")
        dt_mod   = metadata.get("DateTime", "")
        if dt_orig and dt_mod and dt_orig != dt_mod:
            flags.append("DateTime and DateTimeOriginal mismatch — file likely modified after capture")
            score += 25

        # Camera signature
        make  = metadata.get("Make", "")
        model = metadata.get("Model", "")
        if not make and not model:
            flags.append("No camera make/model — possible screenshot or generated image")
            score += 20

        if not flags:
            flags.append("EXIF metadata consistent — no major anomalies detected")

        return {
            "has_exif":     True,
            "metadata":     metadata,
            "flags":        flags,
            "anomaly_score": min(score, 100),
        }
    except Exception as e:
        return {
            "has_exif": False,
            "metadata": {},
            "flags": [f"EXIF read error: {str(e)}"],
            "anomaly_score": 15,
        }


# ─── Noise Analysis ──────────────────────────────────────────

def run_noise_analysis(image_bytes: bytes) -> dict:
    """
    Analyze per-channel noise variance.
    Genuine photos have consistent sensor noise patterns.
    AI-generated or composited images often have unnaturally uniform or patchy noise.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        arr = np.array(img, dtype=np.float32)

        channel_stds = []
        for ch in range(3):
            channel = arr[:, :, ch]
            # High-pass filter to isolate noise
            kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32) / 8.0
            from scipy.signal import convolve2d
            noise_map = convolve2d(channel, kernel, mode="same")
            channel_stds.append(float(np.std(noise_map)))

        mean_noise = float(np.mean(channel_stds))
        noise_balance = float(np.std(channel_stds))  # variation between R/G/B noise

        findings = []
        score = 0

        if mean_noise < 1.5:
            findings.append("Unnaturally low noise — consistent with AI generation or heavy smoothing")
            score += 40
        elif mean_noise > 25:
            findings.append("Unusually high noise — possible artificial grain or JPEG artifacts")
            score += 20

        if noise_balance > 5:
            findings.append("Imbalanced noise across color channels — may indicate compositing")
            score += 25
        else:
            findings.append("Noise distribution balanced across channels")

        return {
            "channel_stds":  [round(s, 3) for s in channel_stds],
            "mean_noise":    round(mean_noise, 3),
            "noise_balance": round(noise_balance, 3),
            "noise_score":   min(score, 100),
            "findings":      findings,
        }
    except ImportError:
        # scipy not installed, fall back
        return _noise_fallback(image_bytes)
    except Exception as e:
        return {"noise_score": 0, "findings": [f"Noise analysis error: {str(e)}"],
                "channel_stds": [], "mean_noise": 0, "noise_balance": 0}


def _noise_fallback(image_bytes: bytes) -> dict:
    """Lightweight noise analysis without scipy."""
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        stat = ImageStat.Stat(img)
        stds = stat.stddev  # R, G, B standard deviations
        mean_noise = sum(stds) / 3
        noise_balance = max(stds) - min(stds)

        findings = []
        score = 0
        if mean_noise < 5:
            findings.append("Low standard deviation — may indicate AI-smoothed image")
            score += 30
        if noise_balance > 20:
            findings.append("High inter-channel variance — possible manipulation")
            score += 20
        else:
            findings.append("Noise levels within expected range")

        return {
            "channel_stds":  [round(s, 3) for s in stds],
            "mean_noise":    round(mean_noise, 3),
            "noise_balance": round(noise_balance, 3),
            "noise_score":   min(score, 100),
            "findings":      findings,
        }
    except Exception as e:
        return {"noise_score": 0, "findings": [str(e)],
                "channel_stds": [], "mean_noise": 0, "noise_balance": 0}


# ─── Compression Artifact Analysis ───────────────────────────

def run_compression_analysis(image_bytes: bytes) -> dict:
    """
    Analyze JPEG compression artifacts.
    Inconsistent block artifacts → multiple saves / compositing.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("L")  # grayscale
        arr = np.array(img, dtype=np.float32)
        h, w = arr.shape

        # Sample 8×8 block boundaries (JPEG DCT blocks)
        h_variances = []
        v_variances = []

        for y in range(0, h - 8, 8):
            for x in range(0, w - 8, 8):
                block = arr[y:y+8, x:x+8]
                h_variances.append(float(np.var(block[0, :] - block[-1, :])))
                v_variances.append(float(np.var(block[:, 0] - block[:, -1])))

        mean_h = float(np.mean(h_variances)) if h_variances else 0
        mean_v = float(np.mean(v_variances)) if v_variances else 0
        block_inconsistency = abs(mean_h - mean_v)

        findings = []
        score = 0

        if block_inconsistency > 50:
            findings.append("High block boundary inconsistency — splicing suspected")
            score += 40
        elif block_inconsistency > 20:
            findings.append("Moderate block inconsistency — possible localized edits")
            score += 20
        else:
            findings.append("Compression artifacts consistent with single-save image")

        return {
            "block_inconsistency": round(block_inconsistency, 2),
            "compression_score":   min(score, 100),
            "findings":            findings,
        }
    except Exception as e:
        return {"block_inconsistency": 0, "compression_score": 0,
                "findings": [f"Compression analysis error: {str(e)}"]}


# ─── Edge & Lighting Analysis ────────────────────────────────

def run_edge_analysis(image_bytes: bytes) -> dict:
    """
    Analyze edge sharpness consistency.
    Spliced images often have abrupt sharpness transitions.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("L")
        edges = img.filter(ImageFilter.FIND_EDGES)
        stat = ImageStat.Stat(edges)

        mean_edge = stat.mean[0]
        std_edge  = stat.stddev[0]
        sharpness_ratio = std_edge / (mean_edge + 1e-5)

        findings = []
        score = 0

        if sharpness_ratio > 8:
            findings.append("Highly variable edge sharpness — inconsistent focus regions")
            score += 30
        elif mean_edge > 80:
            findings.append("Unusually strong edge response — possible over-sharpening")
            score += 20
        else:
            findings.append("Edge sharpness consistent with natural photography")

        return {
            "mean_edge":       round(mean_edge, 2),
            "std_edge":        round(std_edge, 2),
            "sharpness_ratio": round(sharpness_ratio, 2),
            "edge_score":      min(score, 100),
            "findings":        findings,
        }
    except Exception as e:
        return {"mean_edge": 0, "std_edge": 0, "sharpness_ratio": 0,
                "edge_score": 0, "findings": [f"Edge analysis error: {str(e)}"]}


# ─── Master Forensics Runner ──────────────────────────────────

def run_full_image_forensics(image_bytes: bytes) -> dict:
    """
    Run all local forensic analyses and aggregate scores.
    Returns combined forensics dict.
    """
    ela      = run_ela(image_bytes)
    exif     = run_exif_analysis(image_bytes)
    noise    = run_noise_analysis(image_bytes)
    compress = run_compression_analysis(image_bytes)
    edge     = run_edge_analysis(image_bytes)

    # Get image dimensions and metadata
    try:
        img = Image.open(io.BytesIO(image_bytes))
        width, height = img.size
        mode   = img.mode
        format_ = img.format or "Unknown"
    except Exception:
        width, height, mode, format_ = 0, 0, "Unknown", "Unknown"

    # Aggregate manipulation score
    ela_contrib   = ela.get("manipulation_score", 0)     * 0.30
    exif_contrib  = exif.get("anomaly_score", 0)          * 0.20
    noise_contrib = noise.get("noise_score", 0)            * 0.20
    comp_contrib  = compress.get("compression_score", 0)   * 0.15
    edge_contrib  = edge.get("edge_score", 0)              * 0.15

    aggregate_manipulation = int(ela_contrib + exif_contrib + noise_contrib
                                  + comp_contrib + edge_contrib)
    authenticity_score = max(0, 100 - aggregate_manipulation)

    # Collect all findings
    all_findings = []
    all_findings.extend(ela.get("findings", []))
    all_findings.extend(exif.get("flags", []))
    all_findings.extend(noise.get("findings", []))
    all_findings.extend(compress.get("findings", []))
    all_findings.extend(edge.get("findings", []))

    return {
        "manipulation_score":  aggregate_manipulation,
        "authenticity_score":  authenticity_score,
        "image_size":          f"{width} × {height} px",
        "image_mode":          mode,
        "file_size":           f"{len(image_bytes) / 1024:.1f} KB",
        "format":              format_,
        "ela":                 ela,
        "exif":                exif,
        "noise":               noise,
        "compression":         compress,
        "edge":                edge,
        "all_findings":        all_findings,
        "metadata_flags":      exif.get("flags", []),
        "exif_metadata":       exif.get("metadata", {}),
    }
