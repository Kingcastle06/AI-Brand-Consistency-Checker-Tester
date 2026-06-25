from typing import Any, Dict, Optional

class ReportRenderer:
    """
    Local interface wrapper for the report_renderer shared module.
    Responsible for rendering validated structured data into Markdown,
    HTML, DOCX, PDF, or other outputs.
    """
    
    def render_report(self, data: Dict[str, Any], template_id: str, format: str, options: Optional[Dict[str, Any]] = None) -> Any:
        raise NotImplementedError
        
    def export_artifact(self, rendered_content: Any, path: str) -> str:
        raise NotImplementedError
        
    def validate_template(self, template_id: str) -> bool:
        raise NotImplementedError
