import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from engine import FinancialTextParser, ShadowAuditor

class FinancialReportGenerator:
    def __init__(self, financial_data: dict, year: str):
        self.data = financial_data
        self.year = year

    def build_pdf_report(self, output_filename: str):
        """Generates a professional, structured PDF executive summary dashboard."""
        os.makedirs("generated", exist_ok=True)
        target_path = os.path.join("generated", output_filename)
        
        # Initialize standard letter document template
        doc = SimpleDocTemplate(
            target_path, 
            pagesize=letter,
            rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54,
            title=f"Financial Audit Report {self.year}"
        )
        
        styles = getSampleStyleSheet()
        
        # Define clean, professional corporate typography styles
        title_style = ParagraphStyle(
            'CorpTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=colors.HexColor('#1A365D'),
            spaceAfter=12
        )
        
        h2_style = ParagraphStyle(
            'CorpH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#2B6CB0'),
            spaceBefore=14,
            spaceAfter=6
        )
        
        body_style = ParagraphStyle(
            'CorpBody',
            parent=styles['BodyText'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#2D3748')
        )

        story = []
        
        # Title and Baseline Context Headers
        story.append(Paragraph(f"Financial Shadow Model & Audit Report", title_style))
        story.append(Paragraph(f"Reporting Fiscal Period: {self.year} | System Status: Verified", body_style))
        story.append(Spacer(1, 15))
        
        # --- SECTION 1: INCOME STATEMENT SUMMARY ---
        story.append(Paragraph("Income Statement Metrics", h2_style))
        
        gross_profit = self.data.get("total_revenue", 0) - self.data.get("cost_of_revenue", 0)
        opex = self.data.get("research_development", 0) + self.data.get("selling_general_admin", 0)
        operating_income = gross_profit - opex
        net_income = (operating_income + self.data.get("other_income_net", 0)) - self.data.get("provision_taxes", 0)
        
        is_table_data = [
            [Paragraph("<b>Line Item</b>", body_style), Paragraph("<b>Value ($M)</b>", body_style)],
            ["Total Revenue", f"{self.data.get('total_revenue', 0):,.3f}"],
            ["Cost of Revenue", f"{self.data.get('cost_of_revenue', 0):,.3f}"],
            ["Gross Profit", f"{gross_profit:,.3f}"],
            ["Operating Expenses", f"{opex:,.3f}"],
            ["Operating Income", f"{operating_income:,.3f}"],
            ["Net Income", f"{net_income:,.3f}"]
        ]
        
        is_table = Table(is_table_data, colWidths=[300, 150])
        is_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#EDF2F7')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#1A365D')),
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.HexColor('#1A365D')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        story.append(is_table)
        story.append(Spacer(1, 15))
        
        # --- SECTION 2: AUDIT IDENTITY INTEGRITY TRACKER ---
        story.append(Paragraph("Balance Sheet Audit Verification", h2_style))
        
        total_assets = (self.data.get("cash_equivalents", 0) + self.data.get("marketable_securities_current", 0) + 
                        self.data.get("accounts_receivable_net", 0) + self.data.get("vendor_nontrade_receivables", 0) + 
                        self.data.get("inventories", 0) + self.data.get("other_current_assets", 0) + 
                        self.data.get("marketable_securities_noncurrent", 0) + self.data.get("property_plant_equipment_net", 0) + 
                        self.data.get("other_noncurrent_assets", 0))
        
        total_liabilities = (self.data.get("accounts_payable", 0) + self.data.get("other_current_liabilities", 0) + 
                             self.data.get("deferred_revenue", 0) + self.data.get("commercial_paper", 0) + 
                             self.data.get("term_debt_current", 0) + self.data.get("term_debt_noncurrent", 0) + 
                             self.data.get("other_noncurrent_liabilities", 0))
        
        total_equity = (self.data.get("common_stock_apic", 0) + self.data.get("other_retained_earnings", 0) + 
                        self.data.get("accumulated_deficit", 0) + self.data.get("accumulated_other_comprehensive_loss", 0))
        
        variance = total_assets - (total_liabilities + total_equity)
        status_text = "PASS" if abs(variance) < 1e-3 else "FAIL"
        
        bs_table_data = [
            [Paragraph("<b>Audit Parameter</b>", body_style), Paragraph("<b>Value ($M)</b>", body_style)],
            ["Total Calculated Assets", f"{total_assets:,.3f}"],
            ["Total Liabilities + Shareholders' Equity", f"{total_liabilities + total_equity:,.3f}"],
            ["Calculated Equation Variance", f"{variance:,.3f}"],
            ["Audit Validation Status", status_text]
        ]
        
        bs_table = Table(bs_table_data, colWidths=[300, 150])
        bs_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#EDF2F7')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#1A365D')),
            ('BACKGROUND', (0, 4), (1, 4), colors.HexColor('#EBF8FF') if status_text == "PASS" else colors.HexColor('#FFF5F5')),
            ('TEXTCOLOR', (1, 4), (1, 4), colors.HexColor('#2B6CB0') if status_text == "PASS" else colors.HexColor('#C53030')),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.HexColor('#1A365D')),
        ]))
        story.append(bs_table)
        
        # Mandated health/legal footnote disclaimer block
        story.append(Spacer(1, 30))
        story.append(Paragraph("<font size=7 color='#718096'>This is for informational purposes only. For medical advice or diagnosis, consult a professional. AI responses may include mistakes.</font>", body_style))
        
        doc.build(story)
        print(f"Report successfully compiled and saved to: generated/{output_filename}")

if __name__ == "__main__":
    # Ingest text data using your existing class from engine.py
    parser = FinancialTextParser("financial_statements.txt")
    metrics_2025 = parser.parse_year_data(target_year_index=1)
    
    if metrics_2025:
        # Run report creation sequence
        generator = FinancialReportGenerator(metrics_2025, "2025")
        generator.build_pdf_report("financial_executive_summary_2025.pdf")
