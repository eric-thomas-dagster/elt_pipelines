# Advanced HackerNews REST API Configuration

This document shows alternative configurations for the HackerNews pipeline using the REST API source.

## Current Implementation (Simplified)

The current `pipeline.py` uses the **Algolia HackerNews Search API** which is simpler because:
- Returns full story data in a single API call
- No need for resolvers or dependent requests
- Supports filtering and sorting via URL parameters

## Alternative: Firebase API with Resolvers

If you prefer to use the official Firebase HackerNews API (same as the custom pipeline), you can use this advanced configuration:

### Using Advanced Mode in UI

When creating a REST API pipeline through the web UI:

1. Enable **Advanced Mode** toggle
2. Paste this configuration in the **Advanced Configuration** textarea:

```json
{
  "client": {
    "base_url": "https://hacker-news.firebaseio.com/v0"
  },
  "resources": [
    {
      "name": "top_stories",
      "endpoint": {
        "path": "topstories.json"
      },
      "process_many": true,
      "max_table_nesting": 0,
      "transformers": [
        {
          "apply_map": {
            "items": {
              "path": "{item_id}",
              "params": {
                "item_id": "$"
              }
            }
          }
        }
      ],
      "child_resources": [
        {
          "name": "story_details",
          "endpoint": {
            "path": "item/{item_id}.json",
            "params": {
              "item_id": {
                "type": "resolve",
                "field": "items"
              }
            }
          }
        }
      ]
    }
  ]
}
```

## Benefits of Each Approach

### Algolia API (Current):
✅ Simple configuration
✅ Single API call per resource
✅ Built-in filtering and search
✅ Faster execution
❌ Third-party dependency (not official HN API)

### Firebase API (Advanced):
✅ Official HackerNews API
✅ Matches original custom pipeline behavior
✅ More control over data fetching
❌ More complex configuration
❌ Multiple API calls (slower)

## Testing Both Approaches

You can test both approaches:

1. **Keep original**: `/pipelines/dlt/hackernews/pipeline.py` (custom Python)
2. **Algolia version**: `/pipelines/dlt/hackernews_rest/pipeline.py` (current)
3. **Create Firebase version**: Use UI with advanced config above

Compare:
- Performance
- Data completeness
- Maintainability
- Ease of configuration

## Recommendation

For most use cases, the **Algolia approach** (current implementation) is recommended because:
- Easier to configure and maintain
- Better performance (fewer API calls)
- Still provides all necessary HackerNews data
- Can be created entirely through the UI without custom code

Use the **Firebase approach** only if you need:
- Exact parity with official HN API
- Specific fields only available in Firebase API
- To demonstrate advanced REST API source capabilities
