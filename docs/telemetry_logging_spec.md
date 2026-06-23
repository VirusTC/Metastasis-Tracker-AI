# Medical Telemetry Binary Logging Technical Specification (`docs/telemetry_logging_spec.md`)

## 1. Overview
The telemetry architecture handles high-density, low-overhead binary serialization of physiological states. By bypassing bulky string operations or uncompressed structures, it generates a strict file format (`.medbin`) to capture, validate, and chart patient metabolic trajectories across execution loops.

---

## 2. Binary File Layout Architecture

The `.medbin` serialization stream enforces big-endian network structural alignment primitives. Every row block uses exactly 36 bytes of memory, preceded by a global 4-byte magic identity verification header:
