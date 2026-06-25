from typing import Any, Dict, List, Optional

class LLMAdapter:
    """
    Local interface wrapper for the llm_adapter shared module.
    Responsible for routing model calls, enforcing structured output,
    retries, timeouts, cost limits, and provider fallback.
    """
    
    def complete(self, messages: List[Dict[str, Any]], options: Optional[Dict[str, Any]] = None) -> Any:
        raise NotImplementedError

    def complete_structured(self, messages: List[Dict[str, Any]], schema: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        raise NotImplementedError

    def repair_structured_output(self, invalid_output: str, schema: Dict[str, Any], errors: List[str]) -> Dict[str, Any]:
        raise NotImplementedError

    def estimate_cost(self, messages: List[Dict[str, Any]], options: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        raise NotImplementedError
