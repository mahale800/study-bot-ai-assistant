from langchain_core.tools import tool

INFO_DB = {
    "exam_dates": "Finals are Dec 15th to Dec 20th.",
    "library_hours": "Open 8 AM to 10 PM daily.",
    "registrar_email": "registrar@university.edu"
}

@tool
def lookup_info(query: str) -> str:
    """Look up specific university information based on a query.
    
    Useful for finding exam dates, library hours, and registrar email.
    """
    query_lower = query.lower()
    for key, value in INFO_DB.items():
        # Check if key or significant part of key is in query
        # Logic: If a key appears in the query (handling underscores and partial matches for robustness)
        if key in query_lower or key.replace("_", " ") in query_lower or key.split("_")[0] in query_lower:
            return value
    return "Specific data not found in university database."
