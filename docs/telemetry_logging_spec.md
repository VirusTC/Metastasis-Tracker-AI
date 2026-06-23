# Medical Telemetry Binary Logging Technical Specification (`docs/telemetry_logging_spec.md`)

## 1. Overview
The telemetry architecture handles high-density, low-overhead binary serialization of physiological states. By bypassing bulky string operations or uncompressed structures, it generates a strict file format (`.medbin`) to capture, validate, and chart patient metabolic trajectories across execution loops.

---

## 2. Binary File Layout Architecture

The `.medbin` serialization stream enforces big-endian network structural alignment primitives. Every row block uses exactly 36 bytes of memory, preceded by a global 4-byte magic identity verification header:

| BYTE RANGE | DATA VALUE PROPERTY | STRUCT FORMAT PATTERN / ALIGNMENT CONSTRAINT |\
+-------------------+----------------------+---------------------------------------------------+

| Bytes 00 - 03 | Magic Identifier | Big-Endian Unsigned Int (0x4D454442 -> 'MEDB') |\
| Bytes 04 - 07 | Timestep Frame (t) | Big-Endian Unsigned Int (32-bit Integer) |\
| Bytes 08 - 11 | Patient Numeric ID | Big-Endian Unsigned Int (32-bit Integer) |\
| Bytes 12 - 15 | Systemic Plasma pH | Big-Endian IEEE 754 Single-Precision Float |\
| Bytes 16 - 19 | Bicarbonate (HCO3-) | Big-Endian IEEE 754 Single-Precision Float |\
| Bytes 20 - 23 | Serum Calcium (Ca2+) | Big-Endian IEEE 754 Single-Precision Float |\
| Bytes 24 - 27 | Myocardial Force (N) | Big-Endian IEEE 754 Single-Precision Float |\
| Bytes 28 - 31 | CA Enzyme Efficiency | Big-Endian IEEE 754 Single-Precision Float |\
| Bytes 32 - 35 | Gas Pressure (pCO2) | Big-Endian IEEE 754 Single-Precision Float |\
+-------------------+----------------------+---------------------------------------------------+

--- ## 3. Real-Time Error Intercept Boundaries Live sensor telemetry calculations pass through strict constraint gates inside the ingestion class objects. Invalidation traps catch out-of-bounds metrics before they corrupt downstream arrays: * `OutOfBoundsAnatomyError`: Triggered if parameters cross irreversible structural survival thresholds (e.g., \(pCO_2 > 200\text{ mmHg}\)). * `SensorDataCorruptionError`: Triggered if a null, empty, or `NaN` string corrupts the input buffer streams. --- ## 4. Graphics Engine Parsing Matrix To read back data frames or render diagnostic time-series charts, instantiate the automated graphics pipeline mapper from any reporting driver script: ```python from src.graphics_matrix_mapper import GraphicsMatrixMapper # 1. Instantiate the graphics engine mapper target chart_generator = GraphicsMatrixMapper( binary_input_filepath="tests/diagnostic_telemetry.medbin", output_image_path="docs/systemic_patient_trends.png" ) # 2. Parse and generate automated diagnostic subplot grids success = chart_generator.parse_and_plot_history() print(f"Diagnostic Chart Render Completed: {success}") ```
