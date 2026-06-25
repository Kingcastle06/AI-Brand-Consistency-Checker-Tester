from typing import Any, Dict, Optional

class DocumentLoader:
    """
    Local interface wrapper for the document_loader shared module.
    Responsible for converting supported files into normalized text,
    metadata, and extracted structured elements.
    """
    
    def detect_file_type(self, file_reference: Any) -> str:
        raise NotImplementedError
    
    def load_document(self, file_reference: Any, options: Optional[Dict[str, Any]] = None) -> Any:
        raise NotImplementedError
        
    def extract_text(self, document: Any) -> str:
        raise NotImplementedError
        
    def extract_metadata(self, document: Any) -> Dict[str, Any]:
        raise NotImplementedError
