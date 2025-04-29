schema_map = {
    "get_entries": {
      "type": "function",
      "name": "get_entries",
      "description": "Fetch entries from the database using a full text natural language search on the `entry` column, ordered by relevance.",
      "parameters": {
        "type": "object",
        "required": [
          "search_text"
        ],
        "properties": {
          "search_text": {
            "type": "string",
            "description": "Text to search for in the entry column"
          }
        },
        "additionalProperties": False
      },
      "strict": True
    }
}