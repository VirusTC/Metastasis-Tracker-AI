# Myocardial Necrosis Profiles & Compressed JSON Ingestion Specifications

## 1. Overview
This reference standard defines the differential kinetics mapping ischemic cell injury expansion over prolonged zero-flow timelines and standardizes the serialization parameters used to compress data tables into transaction logs.

---

## 2. Mathematical Architecture

### A. Ischemic Tissue Necrosis Volume Expansion
When coronary blood supply drops past critical boundaries ($CBF \le 0.35 \times CBF_{\text{basal}}$), functional muscle volume decays. The accumulation rate of the necrotic tissue mass fraction ($\Omega_{\text{necrosis}}$, fraction) tracks over time increments via:

$$\frac{d\Omega_{\text{necrosis}}(t)}{dt} = \kappa_{\text{necrosis}} \cdot \left( 1.0 - \Omega_{\text{necrosis}}(t) \right) \cdot \left( \frac{\Delta t_{\text{ischemia}}(t)}{\Delta t_{\text{ischemia}}(t) + 180} \right) \times \left(1.0 - \frac{CBF(t)}{0.35 \cdot CBF_{\text{basal}}}\right) \cdot \chi$$

If the cumulative necrotic fraction $\Omega_{\text{necrosis}} \ge 0.40$, the remaining contractile muscle fails, logging an automated `VENTRICULAR_STANDSTILL_ARREST` crisis state to the system registers.

---

## 3. Storage Optimization & Automation Targets

Continuous telemetry readouts are bundled and compressed to minimize disk sector consumption footprint footprints:

### A. GZIP Transaction Packet Packaging
To parse tabular console row records and commit them straight to a compressed binary JSON payload envelope format, run the archiver shortcut:
```bash
make export-json-logs
```
This generates a secure timestamped tracking envelope structure (`src/data/logs/transaction_history_[TIMESTAMP].json.gz`) compressing spatial dataset strings by up to 85%.

### B. Pull Request Link Validation
Relative internal markdown path references inside the `docs/` directory are verified automatically on every pull request check-in using the integration target runner:
```bash
make check-links
```
