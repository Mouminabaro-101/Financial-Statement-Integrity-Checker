# Dynamic Financial Shadow Modeling and Auditing Framework

An automated, data-agnostic financial intelligence engine written in Python. This framework replicates corporate data ingestion pipelines by dynamically scraping unstructured raw text financial statements, standardizing cross-statement line-item anomalies, mapping duplicate variables contextually, and enforcing strict three-statement interlocking accounting audits on the fly.

## Key Architectural Elements
* **Context-Aware Ingestion Pipeline:** Implements a string-splitting text parser that reads files right-to-left to bypass inner-row commas (e.g., handling complex lines like "Selling, general and administrative" without crashing).
* **Sequential Duplicate Router:** Safely tracks duplicate accounting row tags (such as separating short-term and long-term Term Debt or Marketable Securities) based purely on document occurrence sequence.
* **Automated Identity Auditing:** Computes intermediate totals from scratch to perform hard checks on the fundamental accounting identity (Assets match Liabilities + Equity).

## Tech Stack and Dependencies
* **Core Runtime:** Python 3.12+
* **Numerical Constraints and Tolerance Checks:** NumPy (handling floating-point evaluation via np.isclose)

## Execution and Testing Quickstart

### 1. Configure the Isolated Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy
```

### 2. Run the Verification Pipeline
```bash
python3 engine.py
```
