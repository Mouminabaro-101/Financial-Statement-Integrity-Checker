import re
import numpy as np

class FinancialTextParser:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def parse_year_data(self, target_year_index: int = 1) -> dict:
        extracted_data = {}
        
        # Internal counters to handle duplicate rows in sequence
        marketable_securities_count = 0
        term_debt_count = 0

        try:
            with open(self.filepath, "r") as file:
                lines = file.readlines()
                
            for line in lines:
                clean_line = line.replace('"', '').strip()
                if not clean_line:
                    continue
                
                parts = clean_line.split(',')
                # target_year_index=1 (2025) targets the 3rd item from the right end
                right_index = -(4 - target_year_index)
                
                try:
                    val_str = parts[right_index].strip().replace('$', '').replace(' ', '')
                    val = float(val_str)
                except (ValueError, IndexError):
                    continue 
                
                # Extract the row label
                row_name = "".join(parts[:right_index]).strip()

                # --- BULLETPROOF SEQUENTIAL ROUTER ---
                if row_name.lower().startswith("total revenue"):
                    extracted_data["total_revenue"] = val
                elif row_name.lower().startswith("cost of revenue"):
                    extracted_data["cost_of_revenue"] = val
                elif row_name.lower().startswith("research and development"):
                    extracted_data["research_development"] = val
                elif row_name.lower().startswith("selling"):
                    extracted_data["selling_general_admin"] = val
                elif row_name.lower().startswith("other income"):
                    extracted_data["other_income_net"] = val
                elif row_name.lower().startswith("provision for income taxes"):
                    extracted_data["provision_taxes"] = val
                elif row_name.lower().startswith("cash and cash equivalents"):
                    extracted_data["cash_equivalents"] = val
                elif row_name.lower().startswith("accounts receivable"):
                    extracted_data["accounts_receivable_net"] = val
                elif row_name.lower().startswith("vendor non-trade"):
                    extracted_data["vendor_nontrade_receivables"] = val
                elif row_name.lower().startswith("inventories"):
                    extracted_data["inventories"] = val
                elif row_name.lower().startswith("other current assets"):
                    extracted_data["other_current_assets"] = val
                elif row_name.lower().startswith("property"):
                    extracted_data["property_plant_equipment_net"] = val
                elif row_name.lower().startswith("other non-current assets"):
                    extracted_data["other_noncurrent_assets"] = val
                elif row_name.lower().startswith("accounts payable"):
                    extracted_data["accounts_payable"] = val
                elif row_name.lower().startswith("other current liabilities"):
                    extracted_data["other_current_liabilities"] = val
                elif row_name.lower().startswith("deferred revenue"):
                    extracted_data["deferred_revenue"] = val
                elif row_name.lower().startswith("commercial paper"):
                    extracted_data["commercial_paper"] = val
                elif row_name.lower().startswith("other non-current liabilities"):
                    extracted_data["other_noncurrent_liabilities"] = val
                elif row_name.lower().startswith("common stock and additional"):
                    extracted_data["common_stock_apic"] = val
                elif row_name.lower().startswith("accumulated deficit"):
                    extracted_data["accumulated_deficit"] = val
                elif row_name.lower().startswith("accumulated other comprehensive"):
                    extracted_data["accumulated_other_comprehensive_loss"] = val
                elif row_name.lower().startswith("other retained earnings"):
                    extracted_data["other_retained_earnings"] = val
                
                # Handle duplicate rows explicitly based on file order
                elif row_name.lower().startswith("marketable securities"):
                    marketable_securities_count += 1
                    if marketable_securities_count == 1:
                        extracted_data["marketable_securities_current"] = val
                    else:
                        extracted_data["marketable_securities_noncurrent"] = val
                        
                elif row_name.lower().startswith("term debt"):
                    term_debt_count += 1
                    if term_debt_count == 1:
                        extracted_data["term_debt_current"] = val
                    else:
                        extracted_data["term_debt_noncurrent"] = val
            
            return extracted_data
            
        except FileNotFoundError:
            print(f"❌ Error: File {self.filepath} missing.")
            return {}

class ShadowAuditor:
    def __init__(self, data: dict):
        self.data = data

    def run_audit(self, year_label: str):
        yr = self.data
        print(f"\n================ Running Dynamic Audit Pipeline: {year_label} ================")

        # A. Core Income Statement Logic
        gross_profit = yr.get("total_revenue", 0) - yr.get("cost_of_revenue", 0)
        operating_income = gross_profit - (yr.get("research_development", 0) + yr.get("selling_general_admin", 0))
        shadow_net_income = (operating_income + yr.get("other_income_net", 0)) - yr.get("provision_taxes", 0)

        # B. Balanced Asset Aggregation
        total_assets = (yr.get("cash_equivalents", 0) + yr.get("marketable_securities_current", 0) + 
                        yr.get("accounts_receivable_net", 0) + yr.get("vendor_nontrade_receivables", 0) + 
                        yr.get("inventories", 0) + yr.get("other_current_assets", 0) + 
                        yr.get("marketable_securities_noncurrent", 0) + yr.get("property_plant_equipment_net", 0) + 
                        yr.get("other_noncurrent_assets", 0))
        
        # C. Balanced Liabilities Aggregation
        total_liabilities = (yr.get("accounts_payable", 0) + yr.get("other_current_liabilities", 0) + 
                             yr.get("deferred_revenue", 0) + yr.get("commercial_paper", 0) + 
                             yr.get("term_debt_current", 0) + yr.get("term_debt_noncurrent", 0) + 
                             yr.get("other_noncurrent_liabilities", 0))
        
        # D. Balanced Equity Aggregation
        total_equity = (yr.get("common_stock_apic", 0) + yr.get("other_retained_earnings", 0) + 
                        yr.get("accumulated_deficit", 0) + yr.get("accumulated_other_comprehensive_loss", 0))

        accounting_identity_variance = total_assets - (total_liabilities + total_equity)

        print(f"Parsed Shadow Net Income: ${round(shadow_net_income, 3)}M")
        print(f"Total Calculated Assets: ${round(total_assets, 3)}M")
        print(f"Total Liabilities + Equity: ${round(total_liabilities + total_equity, 3)}M")
        
        if np.isclose(accounting_identity_variance, 0.0, atol=1e-3):
            print("✅ PASS: Data parsed perfectly. The accounting identity balances.")
        else:
            print(f"❌ FAIL: Balance Sheet Discrepancy Found! Variance: ${round(accounting_identity_variance, 3)}M")

if __name__ == "__main__":
    parser = FinancialTextParser("financial_statements.txt")
    parsed_2025_metrics = parser.parse_year_data(target_year_index=1)
    
    if parsed_2025_metrics:
        engine = ShadowAuditor(parsed_2025_metrics)
        engine.run_audit("2025")
