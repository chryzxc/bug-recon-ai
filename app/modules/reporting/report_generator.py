from jinja2 import Environment, FileSystemLoader
import pdfkit
import matplotlib.pyplot as plt
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self, template_dir='templates'):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
    def generate_html_report(self, scan_results, template_name='report_template.html'):
        template = self.env.get_template(template_name)
        
        report_data = {
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'target': scan_results.get('target', 'Unknown'),
            'findings': scan_results.get('findings', []),
            'summary': scan_results.get('summary', 'No summary available')
        }
        
        return template.render(report_data)
    
    def generate_pdf_report(self, scan_results, output_path='report.pdf'):
        html = self.generate_html_report(scan_results)
        
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
        }
        
        pdfkit.from_string(html, output_path, options=options)
        return output_path
    
    def generate_visualizations(self, findings, output_dir='visualizations'):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Severity distribution pie chart
        severities = [f['severity'] for f in findings]
        severity_counts = {s: severities.count(s) for s in set(severities)}
        
        plt.figure(figsize=(8, 6))
        plt.pie(severity_counts.values(), labels=severity_counts.keys(), autopct='%1.1f%%')
        plt.title('Vulnerability Severity Distribution')
        severity_chart_path = os.path.join(output_dir, 'severity_distribution.png')
        plt.savefig(severity_chart_path)
        plt.close()
        
        return severity_chart_path