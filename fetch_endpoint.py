import requests
import json
from datetime import datetime
import time
import os
from pathlib import Path

class ON24DocRetriever:
    def __init__(self, output_dir="on24_docs"):
        self.base_url = "https://apidoc.on24.com"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://apidoc.on24.com/"
        }
        
        # Common query parameters
        self.common_params = {
            "company_id": "291",
            "project_id": "13630",
            "parent_id": "0",
            "ui_lang": "en",
            "prim_index": "0",
            "view_mode": "view",
            "user_index": "false",
            "preview": "",
            "inst_preview": "false"
        }

    def get_timestamp(self):
        return int(datetime.now().timestamp() * 1000)

    def fetch_toc_tree(self, node_id):
        """Fetch the TOC tree for a given node ID."""
        params = {
            **self.common_params,
            "_dc": self.get_timestamp(),
            "node": node_id,
            "r_req": "true"
        }
        
        url = f"{self.base_url}/topic/nav/load_toc_tree/"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching TOC tree for node {node_id}: {e}")
            return None

    def fetch_content(self, permalink):
        """Fetch content for a given permalink."""
        params = {
            **self.common_params,
            "_dc": self.get_timestamp(),
            "id": permalink,
            "highlight_keyword": "",
            "script_indexs[]": "",
            "r_req": "true"
        }
        
        url = f"{self.base_url}/topic/get_content/"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching content for permalink {permalink}: {e}")
            return None

    def save_content(self, content, section_path, title):
        """Save content to a file."""
        # Create section directory if it doesn't exist
        save_dir = self.output_dir / section_path
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a safe filename from the title
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')
        
        # Save both raw JSON and extracted HTML content
        json_file = save_dir / f"{safe_title}.json"
        html_file = save_dir / f"{safe_title}.html"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)
        
        if content.get('success') and content.get('data', {}).get('content'):
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content['data']['content'])

    def process_folder(self, folder_id, section_path):
        """Process a folder and all its contents."""
        print(f"Processing folder: {folder_id} in {section_path}")
        
        # Get the TOC tree for this folder
        toc_tree = self.fetch_toc_tree(folder_id)
        if not toc_tree:
            return
        
        time.sleep(1)  # Be nice to the server
        
        for item in toc_tree:
            item_type = item.get('type', '')
            item_id = item.get('id', '')
            item_text = item.get('text', '')
            permalink = item.get('permalink', '')
            
            if item_type == 'folder':
                # Process subfolders recursively
                new_section_path = f"{section_path}/{item_text}"
                self.process_folder(f"f;{item_id}", new_section_path)
            elif permalink:
                # Fetch and save content for this item
                print(f"Fetching content: {item_text}")
                content = self.fetch_content(permalink)
                if content:
                    self.save_content(content, section_path, item_text)
                time.sleep(1)  # Be nice to the server

    def crawl(self):
        """Start the crawling process from the root."""
        print("Starting documentation crawl...")
        self.process_folder("1906713", "root")
        print("Crawl completed!")

if __name__ == "__main__":
    retriever = ON24DocRetriever()
    retriever.crawl() 