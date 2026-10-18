import os
import matplotlib.pyplot as plt
from engine import FinancialTextParser

def generate_financial_charts():
    # 1. Read your data using your existing text parser
    parser = FinancialTextParser("financial_statements.txt")
    data = parser.parse_year_data(target_year_index=1) # 2025 data
    
    if not data:
        print("❌ Error: No data found to visualize.")
        return

    # 2. Calculate core sections for the chart
    total_current_assets = (data.get("cash_equivalents", 0) + 
                            data.get("marketable_securities_current", 0) + 
                            data.get("accounts_receivable_net", 0) + 
                            data.get("vendor_nontrade_receivables", 0) + 
                            data.get("inventories", 0) + 
                            data.get("other_current_assets", 0))
    
    total_noncurrent_assets = data.get("marketable_securities_noncurrent", 0) + data.get("property_plant_equipment_net", 0) + data.get("other_noncurrent_assets", 0)
    
    total_current_liabilities = (data.get("accounts_payable", 0) + 
                                 data.get("other_current_liabilities", 0) + 
                                 data.get("deferred_revenue", 0) + 
                                 data.get("commercial_paper", 0) + 
                                 data.get("term_debt_current", 0))
    
    total_noncurrent_liabilities = data.get("term_debt_noncurrent", 0) + data.get("other_noncurrent_liabilities", 0)
    
    total_equity = (data.get("common_stock_apic", 0) + 
                    data.get("other_retained_earnings", 0) + 
                    data.get("accumulated_deficit", 0) + 
                    data.get("accumulated_other_comprehensive_loss", 0))

    # 3. Setup the visual layout (Bar Chart)
    categories = ['Current Assets', 'Non-Current Assets', 'Current Liabilities', 'Non-Current Liabilities', 'Total Equity']
    values = [total_current_assets, total_noncurrent_assets, total_current_liabilities, total_noncurrent_liabilities, total_equity]
    colors = ['#2B6CB0', '#4299E1', '#C53030', '#F56565', '#48BB78']

    plt.figure(figsize=(10, 5))
    bars = plt.bar(categories, values, color=colors, edgecolor='black', linewidth=0.7)
    
    # Style the chart cleanly
    plt.title('Balance Sheet Structural Breakdown (2025 Fiscal Year)', fontsize=14, pad=15, fontweight='bold')
    plt.ylabel('Value ($ Millions)', fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Add exact value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                 f"${round(height, 1)}M",
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    
    # 4. Save the visual chart as a PNG image file
    os.makedirs("images", exist_ok=True)
    image_path = "images/balance_sheet_breakdown.png"
    plt.savefig(image_path, dpi=300)
    plt.close()
    print(f"✅ Success: Visual chart saved to {image_path}")

if __name__ == "__main__":
    generate_financial_charts()
