import json
import os
import logging
from src.json_utils import safe_parse_json

logger = logging.getLogger(__name__)

class Visualizer:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir

    def generate_dependency_diagram(self, results):
        """Generates a Mermaid dependency diagram from analysis results."""
        diagram_path = os.path.join(self.output_dir, "dependency_graph.mmd")
        
        nodes = set()
        edges = set()

        for filename, data in results.items():
            analysis_text = data.get('analysis', '')
            if not analysis_text or analysis_text.startswith("Error"):
                continue

            try:
                # Use safe JSON parsing with repair
                info = safe_parse_json(analysis_text)
                if not info:
                    logger.warning(f"Could not parse JSON for {filename}")
                    continue
                
                # Node Identification
                node_name = None
                node_type = "unknown"

                if "table_name" in info:
                    node_name = info["table_name"]
                    node_type = "table"
                elif "procedure_name" in info:
                    node_name = info["procedure_name"]
                    node_type = "procedure"
                elif "mapping_name" in info:
                    node_name = info["mapping_name"] or filename # Fallback if null
                    node_type = "mapping"
                
                if node_name:
                    nodes.add((node_name, node_type))

                    # Edge Identification
                    # 1. Foreign Keys (Table -> Table)
                    if "foreign_keys" in info:
                        for fk in info["foreign_keys"]:
                            if isinstance(fk, dict) and "referenced_table" in fk:
                                edges.add((node_name, fk["referenced_table"], "FK"))
                    
                    # 2. SP Dependencies (SP -> Table/SP)
                    if "tables_read" in info:
                        for tbl in info["tables_read"]:
                            edges.add((node_name, tbl, "READS"))
                    if "tables_modified" in info:
                        for tbl in info["tables_modified"]:
                            edges.add((node_name, tbl, "MODIFIES"))
                    if "dependencies" in info:
                        for dep in info["dependencies"]:
                            edges.add((node_name, dep, "CALLS"))

                    # 3. Mapping Dependencies (Mapping -> Table)
                    if "sources" in info:
                        for src in info["sources"]:
                            edges.add((src, node_name, "SOURCE"))
                    if "targets" in info:
                        for tgt in info["targets"]:
                            edges.add((node_name, tgt, "TARGET"))

            except json.JSONDecodeError:
                logger.warning(f"Could not parse JSON for {filename}")
                continue
            except Exception as e:
                logger.warning(f"Error processing {filename}: {e}")
                continue

        # Generate Mermaid Content
        mermaid_content = "graph TD\n"
        
        # Styles
        mermaid_content += "    classDef table fill:#e1f5fe,stroke:#01579b,stroke-width:2px;\n"
        mermaid_content += "    classDef procedure fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;\n"
        mermaid_content += "    classDef mapping fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;\n"

        # Nodes
        for name, type_ in nodes:
            safe_name = self._sanitize_id(name)
            mermaid_content += f"    {safe_name}[{name}]:::{type_}\n"

        # Edges
        for src, dst, label in edges:
            safe_src = self._sanitize_id(src)
            safe_dst = self._sanitize_id(dst)
            # Only add edge if both nodes exist (or maybe we want to show external deps?)
            # For now, let's show all to see missing deps too
            mermaid_content += f"    {safe_src} -->|{label}| {safe_dst}\n"

        with open(diagram_path, "w") as f:
            f.write(mermaid_content)
        
        print(f"Dependency diagram generated at: {diagram_path}")

    def _sanitize_id(self, text):
        """Sanitizes text to be a valid Mermaid ID."""
        return text.replace(" ", "_").replace("-", "_").replace(".", "_").replace("$", "")
