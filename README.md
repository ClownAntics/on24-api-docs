Copyright © ON24. All rights reserved.
This documentation is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

# ON24 API Documentation Retriever

## Overview
This tool retrieves documentation content from the ON24 API documentation portal. The documentation is structured as a React SPA (Single Page Application) with content being loaded dynamically through API calls.

## How the ON24 Documentation Portal Works

### Content Structure
- The documentation is organized in a hierarchical tree structure
- Each piece of content has both a numeric ID and a permalink
- Content must be retrieved using permalinks rather than numeric IDs
- The tree structure has multiple levels (e.g., Analytics > Client Level > Attendees)

### Required Parameters
All content requests require the following query parameters:
- `_dc`: Current timestamp in milliseconds
- `company_id`: 291
- `project_id`: 13630
- `parent_id`: 0
- `ui_lang`: en
- `prim_index`: 0
- `view_mode`: view
- `user_index`: false
- `preview`: empty string
- `inst_preview`: false

### Content Retrieval Process
1. Get the main Table of Contents (TOC) tree
2. Navigate through the TOC tree to find the desired section
3. Get the TOC tree for the specific section
4. Use the permalink from the TOC tree to retrieve the actual content

### API Endpoints

#### TOC Tree Endpoint
```
GET /topic/nav/load_toc_tree/
```
Parameters:
- All required parameters listed above
- `node`: Folder ID (e.g., "f;143002" for Analytics section)

#### Content Endpoint
```
GET /topic/get_content/
```
Parameters:
- All required parameters listed above
- `id`: The permalink of the content to retrieve

### Response Format
Content responses include:
- `success`: Boolean indicating if the request was successful
- `data.content`: HTML content of the documentation
- Various metadata about the page

## Implementation Notes

### Headers Required
```python
headers = {
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://apidoc.on24.com/"
}
```

### Content Retrieval Steps
1. First get the TOC tree to find the correct permalink
2. Use the permalink to get the actual content
3. Parse and process the HTML content as needed

## Usage
```python
python fetch_endpoint.py
```

## Limitations
- Content must be retrieved using permalinks, not numeric IDs
- Each request requires specific query parameters
- The documentation portal is a React SPA, so content is loaded dynamically
- Some content may require session cookies or authentication 