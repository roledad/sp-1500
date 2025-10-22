"""
Document Assets Manager
Utility functions for managing downloaded proxy documents in doc_assets folder
"""

import os
import glob
from datetime import datetime
from typing import List, Dict


class DocAssetsManager:
    """Manager for document assets in doc_assets folder"""

    def __init__(self, doc_assets_dir: str = "doc_assets"):
        """
        Initialize the document assets manager

        Args:
            doc_assets_dir: Path to the doc_assets directory
        """
        self.doc_assets_dir = doc_assets_dir
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        """Ensure the doc_assets directory exists"""
        os.makedirs(self.doc_assets_dir, exist_ok=True)

    def list_proxy_documents(self) -> List[Dict[str, str]]:
        """
        List all proxy documents in the doc_assets folder

        Returns:
            List of dictionaries with document information
        """
        if not os.path.exists(self.doc_assets_dir):
            return []

        proxy_files = glob.glob(os.path.join(self.doc_assets_dir, "proxy_*.pdf"))
        documents = []

        for file_path in proxy_files:
            filename = os.path.basename(file_path)
            stat = os.stat(file_path)

            documents.append({
                'filename': filename,
                'path': file_path,
                'size_bytes': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })

        # Sort by creation time (newest first)
        documents.sort(key=lambda x: x['created'], reverse=True)
        return documents

    def cleanup_old_documents(self, days_old: int = 30):
        """
        Clean up old proxy documents

        Args:
            days_old: Remove documents older than this many days
        """
        documents = self.list_proxy_documents()
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)

        removed_count = 0
        for doc in documents:
            file_stat = os.stat(doc['path'])
            if file_stat.st_ctime < cutoff_time:
                try:
                    os.remove(doc['path'])
                    removed_count += 1
                    print(f"Removed old document: {doc['filename']}")
                except Exception as e:
                    print(f"Error removing {doc['filename']}: {e}")

        print(f"Cleaned up {removed_count} old documents")

    def get_document_info(self, filename: str) -> Dict[str, str]:
        """
        Get information about a specific document

        Args:
            filename: Name of the document file

        Returns:
            Dictionary with document information
        """
        file_path = os.path.join(self.doc_assets_dir, filename)

        if not os.path.exists(file_path):
            return {'error': f'Document {filename} not found'}

        stat = os.stat(file_path)

        return {
            'filename': filename,
            'path': file_path,
            'size_bytes': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'exists': True
        }

    def get_storage_usage(self) -> Dict[str, float]:
        """
        Get storage usage information for doc_assets folder

        Returns:
            Dictionary with storage usage information
        """
        documents = self.list_proxy_documents()

        total_size_bytes = sum(doc['size_bytes'] for doc in documents)
        total_size_mb = round(total_size_bytes / (1024 * 1024), 2)
        total_size_gb = round(total_size_mb / 1024, 2)

        return {
            'total_documents': len(documents),
            'total_size_bytes': total_size_bytes,
            'total_size_mb': total_size_mb,
            'total_size_gb': total_size_gb
        }


def main():
    """Example usage of the document assets manager"""
    manager = DocAssetsManager()

    print("Document Assets Manager")
    print("=" * 30)

    # List all documents
    documents = manager.list_proxy_documents()
    print(f"\nFound {len(documents)} proxy documents:")

    for doc in documents[:5]:  # Show first 5
        print(f"  {doc['filename']} ({doc['size_mb']} MB) - {doc['created']}")

    if len(documents) > 5:
        print(f"  ... and {len(documents) - 5} more")

    # Show storage usage
    usage = manager.get_storage_usage()
    print(f"\nStorage Usage:")
    print(f"  Total documents: {usage['total_documents']}")
    print(f"  Total size: {usage['total_size_mb']} MB ({usage['total_size_gb']} GB)")

    # Optionally clean up old documents
    if len(documents) > 10:
        print(f"\nYou have {len(documents)} documents. Consider cleaning up old ones:")
        print("manager.cleanup_old_documents(days_old=30)")


if __name__ == "__main__":
    main()
