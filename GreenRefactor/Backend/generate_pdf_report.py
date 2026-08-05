"""
Generate PDF / Printable Academic Research Report for GreenRefactor Benchmarks.

Usage:
    python generate_pdf_report.py
Output:
    Backend/results/GreenRefactor_Research_Report.html
    (Can be printed or saved directly as PDF from browser or CLI)
"""
import json
import os
import sys

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
SUMMARY_PATH = os.path.join(RESULTS_DIR, "comparison_summary.json")

def generate_report():
    if not os.path.isfile(SUMMARY_PATH):
        # Generate summary first if needed
        from compare_results import main as generate_summary
        generate_summary()

    if not os.path.isfile(SUMMARY_PATH):
        print(f"Error: {SUMMARY_PATH} not found. Run run_language_batch.py first.")
        return

    with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    exp_info = data.get("experiment_info", {})
    overall = data.get("overall_stats", {})
    rq1 = data.get("rq1_language_summary", {})
    rq2 = data.get("rq2_runtime_summary", {})
    rows = data.get("rows", [])

    rows_html = ""
    for r in rows:
        sig_badge = '<span style="color:#059669; font-weight:bold;">Yes (p &lt; 0.05)</span>' if r.get("significant") else '<span style="color:#64748b;">No</span>'
        pct = r.get("percent_change", 0)
        pct_str = f"{pct:.2f}%" if pct <= 0 else f"+{pct:.2f}%"
        color = "#059669" if pct <= 0 else "#dc2626"
        rows_html += f"""
        <tr>
            <td style="font-weight:600; text-transform:uppercase;">{r.get('language')}</td>
            <td>{r.get('runtime_category')}</td>
            <td style="font-weight:600;">{r.get('repo')}</td>
            <td><code>{r.get('pattern')}</code></td>
            <td style="font-weight:bold; color:{color};">{pct_str}</td>
            <td>{r.get('p_value', 0):.4f}</td>
            <td>{r.get('cohens_d', 0):.2f}</td>
            <td>{sig_badge}</td>
        </tr>
        """

    rq1_html = ""
    for lang, summary in rq1.items():
        rq1_html += f"""
        <tr>
            <td style="font-weight:600; text-transform:uppercase;">{lang}</td>
            <td>{summary.get('repos', 0)}</td>
            <td style="font-weight:bold; color:#059669;">-{summary.get('mean_savings_percent', 0):.1f}%</td>
            <td>{summary.get('significant_count', 0)}</td>
            <td>d = {summary.get('avg_cohens_d', 0):.2f}</td>
            <td><code>{summary.get('primary_pattern', 'N/A')}</code></td>
        </tr>
        """

    rq2_html = ""
    for cat, summary in rq2.items():
        rq2_html += f"""
        <tr>
            <td style="font-weight:600;">{cat}</td>
            <td>{summary.get('repos', 0)}</td>
            <td style="font-weight:bold; color:#059669;">-{summary.get('mean_savings_percent', 0):.1f}%</td>
            <td>d = {summary.get('avg_cohens_d', 0):.2f}</td>
            <td><span style="background:#d1fae5; color:#065f46; padding:2px 8px; border-radius:4px; font-weight:600; font-size:12px;">{summary.get('impact_rating', 'Moderate')} Impact</span></td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>GreenRefactor_Empirical_Research_Report</title>
    <style>
        @page {{ size: A4; margin: 20mm; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.5; margin: 30px; background: #fff; }}
        .header {{ border-bottom: 3px solid #10b981; padding-bottom: 16px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-end; }}
        h1 {{ font-size: 24px; color: #064e3b; margin: 0; font-weight: 800; letter-spacing: -0.02em; }}
        .subtitle {{ font-size: 13px; color: #64748b; margin-top: 4px; }}
        .badge-head {{ background: #065f46; color: #fff; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 12px; display: inline-block; }}
        
        .metrics-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 28px; }}
        .metric-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: center; }}
        .metric-val {{ font-size: 22px; font-weight: 800; color: #059669; }}
        .metric-label {{ font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600; margin-top: 4px; letter-spacing: 0.05em; }}
        
        h2 {{ font-size: 16px; color: #0f172a; margin-top: 28px; margin-bottom: 12px; border-left: 4px solid #10b981; padding-left: 10px; font-weight: 700; }}
        
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 12px; }}
        th, td {{ border: 1px solid #e2e8f0; padding: 8px 12px; text-align: left; }}
        th {{ background: #f1f5f9; font-weight: 700; color: #334155; text-transform: uppercase; font-size: 11px; letter-spacing: 0.03em; }}
        tr:nth-child(even) {{ background: #fafafa; }}
        
        code {{ font-family: "Courier New", Courier, monospace; background: #e2e8f0; padding: 2px 5px; border-radius: 4px; font-size: 11px; }}
        
        .footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid #cbd5e1; font-size: 11px; color: #94a3b8; text-align: center; }}
        
        .print-btn {{ background: #10b981; color: white; border: none; padding: 10px 18px; border-radius: 6px; font-weight: 700; cursor: pointer; float: right; margin-bottom: 20px; }}
        @media print {{ .print-btn {{ display: none; }} body {{ margin: 0; }} }}
    </style>
</head>
<body>

    <button class="print-btn" onclick="window.print()">🖨️ Save / Export as PDF</button>

    <div class="header">
        <div>
            <h1>GreenRefactor — Empirical Research Benchmark Report</h1>
            <div class="subtitle">Automated Multi-Language Green Code Refactoring & Energy Savings Telemetry</div>
        </div>
        <div>
            <span class="badge-head">RAPL / TDP Telemetry</span>
        </div>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-val">-{overall.get('mean_energy_savings_pct', 0)}%</div>
            <div class="metric-label">Mean Energy Savings</div>
        </div>
        <div class="metric-card">
            <div class="metric-val" style="color: #4f46e5;">{overall.get('total_refactors_applied', 0)}</div>
            <div class="metric-label">Refactors Applied & Measured</div>
        </div>
        <div class="metric-card">
            <div class="metric-val" style="color: #0284c7;">{overall.get('significant_refactor_rate_pct', 0)}%</div>
            <div class="metric-label">Statistically Sig. Rate</div>
        </div>
        <div class="metric-card">
            <div class="metric-val" style="color: #d97706;">d = {overall.get('avg_effect_size_cohens_d', 0)}</div>
            <div class="metric-label">Avg Cohen's d Effect Size</div>
        </div>
    </div>

    <h2>RQ1: Language-Specific Energy Savings Summary</h2>
    <table>
        <thead>
            <tr>
                <th>Language</th>
                <th>Repos Evaluated</th>
                <th>Mean Savings (%)</th>
                <th>Statistically Sig. Refactors</th>
                <th>Avg Cohen's d</th>
                <th>Primary Pattern</th>
            </tr>
        </thead>
        <tbody>
            {rq1_html}
        </tbody>
    </table>

    <h2>RQ2: Runtime Category Energy Savings Comparison</h2>
    <table>
        <thead>
            <tr>
                <th>Runtime Category</th>
                <th>Repos Evaluated</th>
                <th>Mean Savings (%)</th>
                <th>Avg Cohen's d</th>
                <th>Impact Rating</th>
            </tr>
        </thead>
        <tbody>
            {rq2_html}
        </tbody>
    </table>

    <h2>RQ3: Detailed Case-by-Case Experimental Measurements</h2>
    <table>
        <thead>
            <tr>
                <th>Language</th>
                <th>Category</th>
                <th>Repository</th>
                <th>Pattern</th>
                <th>Energy Change</th>
                <th>p-value (Wilcoxon)</th>
                <th>Cohen's d</th>
                <th>Statistically Significant</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>

    <div class="footer">
        Generated automatically by GreenRefactor Platform • Empirical Software Engineering & Sustainable Computing Benchmark Suite
    </div>

</body>
</html>
"""

    out_path = os.path.join(RESULTS_DIR, "GreenRefactor_Research_Report.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Research Report PDF/HTML successfully generated at:")
    print(f"   {out_path}")
    print("\n💡 Open this file in your browser and press Ctrl+P -> 'Save as PDF' to produce the PDF file.")

if __name__ == "__main__":
    generate_report()
