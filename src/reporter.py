import json
import os

class Reporter:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_report(self, results):
        """Generates a report from analysis results."""
        # Save raw results to JSON
        json_path = os.path.join(self.output_dir, "analysis_results.json")
        with open(json_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Raw results saved to: {json_path}")

        report_path = os.path.join(self.output_dir, "analysis_report.txt")
        
        with open(report_path, "w") as f:
            f.write("Sybase Analysis Report\n\n")
            
            for filename, data in results.items():
                f.write(f"File: {filename}\n")
                f.write(f"Type: {data['type']}\n\n")
                
                analysis = data['analysis']
                if analysis.startswith("Error"):
                    f.write(f"[!WARNING]\n{analysis}\n\n")
                else:
                    # Try to format JSON if it looks like JSON
                    try:
                        # Remove potential markdown code blocks
                        clean_analysis = analysis.replace("```json", "").replace("```", "")
                        json_data = json.loads(clean_analysis)
                        f.write("Analysis Summary (JSON)\n")
                        f.write(f"{json.dumps(json_data, indent=2)}\n\n")
                    except json.JSONDecodeError:
                        f.write("Raw Analysis\n")
                        f.write(f"{analysis}\n\n")
        
        print(f"Report generated at: {report_path}")
