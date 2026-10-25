# Financial-Statement-Integrity-Check

A Python tool that extracts line items from a raw-text financial statement, rebuilds the key totals independently, and tests whether the accounting identity holds: Assets = Liabilities + Equity.

## Why this exists

When financial data is pulled from raw text, one misread row silently corrupts every ratio computed afterwards. This project adds a check at the point of extraction. If the rebuilt balance sheet does not balance, something was misparsed or is missing.

## What it does

1. Parses a text file of financial statements and maps each line item (revenue, cost of revenue, R&D, receivables, debt, equity components and others) to a named field.
2. Rebuilds the figures from those line items: gross profit, operating income and net income (the "shadow" net income), plus total assets, total liabilities and total equity.
3. Tests the accounting identity within a tolerance of 0.001 in the file's units. With figures in millions, that is $1,000.
4. Reports PASS or FAIL, with the size of the variance on failure.

## Example output

A successful run prints the shadow net income, the total calculated assets, and the total of liabilities plus equity, then this line:

```
✅ PASS: Data parsed perfectly. The accounting identity balances.
```

If a value in the input file is wrong or missing, the tool prints a failure line instead, with the amount by which the two sides differ:

```
❌ FAIL: Balance Sheet Discrepancy Found!
```

To see the failure case yourself, change any single number in the input file and run the tool again.

## Project structure

```
engine.py                 Parser and auditor classes, plus the entry point
financial_statements.txt  Sample input file
requirements.txt          Python dependencies
```

## How to run

Requires Python 3.8 or later.

```bash
git clone https://github.com/Mouminabaro-101/shadow-model-financial-audit.git
cd shadow-model-financial-audit
pip install -r requirements.txt
python engine.py
```

The `requirements.txt` file contains a single line: `numpy`.

## How it works

`FinancialTextParser` reads the file line by line, strips quotes, splits each row on commas, and selects the year column by its position counted from the right end of the row. Row labels are matched by prefix. Labels that appear twice in the file, marketable securities and term debt, are assigned to current and non-current in the order they appear.

`ShadowAuditor` recomputes the totals from the extracted fields and compares total assets with total liabilities plus equity, using `numpy.isclose` for the tolerance test.

## Limitations

- Built around one statement layout. Row labels and column positions are hard-coded.
- A line item not found in the file defaults to zero, so the failure message does not name the missing field.
- Values written in parentheses, such as (1,234), are not parsed. Negative numbers must use a minus sign.
- The identity check shows that the extraction is complete and internally consistent. It does not compare the results against the totals reported by the company.

## Roadmap

- Compare the rebuilt net income and total assets against the reported figures
- Raise an explicit error that lists any missing line items
- Read the year from the header row instead of passing it in manually
- Add pytest tests, including a corrupted-input case that must fail
- Extend the tool to the cash flow statement and check the links between statements

## Author

Mouminatou Baro

GitHub: https://github.com/Mouminabaro-101
