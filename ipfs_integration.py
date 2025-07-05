#!/usr/bin/env python3
"""
PeerAI IPFS Integration System
نظام دمج PeerAI مع IPFS
"""

import asyncio
import json
import hashlib
import logging
import os
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import torch
import pickle
import ipfshttpclient
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class IPFSModelMetadata:
    """IPFS model metadata structure"""
    model_id: str
    model_type: str
    cid: str  # IPFS Content Identifier
    created_at: str
    uploaded_at: str
    file_size: int
    model_hash: str
    node_id: str
    accuracy: Optional[float] = None
    training_data_hash: Optional[str] = None
    description: Optional[str] = None

@dataclass
class IPFSDataMetadata:
    """IPFS data metadata structure"""
    data_id: str
    cid: str
    created_at: str
    uploaded_at: str
    file_size: int
    data_type: str
    node_id: str
    sample_count: Optional[int] = None
    features: Optional[List[str]] = None
    description: Optional[str] = None

class PeerAIIPFS:
    """IPFS integration for PeerAI system"""
    
    def __init__(self, ipfs_host: str = 'localhost', ipfs_port: int = 5001):
        """Initialize IPFS client"""
        self.ipfs_host = ipfs_host
        self.ipfs_port = ipfs_port
        
        # IPFS client
        try:
            self.client = ipfshttpclient.connect(f'/ip4/{ipfs_host}/tcp/{ipfs_port}/http')
            logger.info(f"Connected to IPFS node at {ipfs_host}:{ipfs_port}")
        except Exception as e:
            logger.error(f"Failed to connect to IPFS: {e}")
            self.client = None
        
        # Local storage
        self.storage_dir = Path(".peerai_ipfs")
        self.storage_dir.mkdir(exist_ok=True)
        
        self.models_dir = self.storage_dir / "models"
        self.data_dir = self.storage_dir / "data"
        self.metadata_dir = self.storage_dir / "metadata"
        
        for dir_path in [self.models_dir, self.data_dir, self.metadata_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Metadata files
        self.models_metadata_file = self.metadata_dir / "models.json"
        self.data_metadata_file = self.metadata_dir / "data.json"
        
        # Load existing metadata
        self.models_metadata = self._load_metadata(self.models_metadata_file)
        self.data_metadata = self._load_metadata(self.data_metadata_file)
    
    def _load_metadata(self, metadata_file: Path) -> Dict:
        """Load metadata from file"""
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_metadata(self, metadata: Dict, metadata_file: Path):
        """Save metadata to file"""
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    async def upload_model(self, model_path: Path, model_info: Dict, node_id: str) -> Dict:
        """Upload a PyTorch model to IPFS"""
        if not self.client:
            raise ConnectionError("IPFS client not connected")
        
        try:
            # Create a package with model and metadata
            package_path = await self._create_model_package(model_path, model_info)
            
            # Upload to IPFS
            result = self.client.add(str(package_path))
            cid = result['Hash']
            
            # Create metadata
            file_size = package_path.stat().st_size
            model_hash = self._calculate_file_hash(package_path)
            
            metadata = IPFSModelMetadata(
                model_id=model_info.get('model_id', 'unknown'),
                model_type=model_info.get('type', 'unknown'),
                cid=cid,
                created_at=model_info.get('created_at', datetime.now().isoformat()),
                uploaded_at=datetime.now().isoformat(),
                file_size=file_size,
                model_hash=model_hash,
                node_id=node_id,
                accuracy=model_info.get('final_accuracy'),
                description=model_info.get('description')
            )
            
            # Save metadata
            self.models_metadata[cid] = asdict(metadata)
            self._save_metadata(self.models_metadata, self.models_metadata_file)
            
            # Clean up temporary package
            package_path.unlink()
            
            logger.info(f"Model uploaded to IPFS: {cid}")
            return {
                'cid': cid,
                'metadata': asdict(metadata),
                'ipfs_url': f'https://ipfs.io/ipfs/{cid}'
            }
        
        except Exception as e:
            logger.error(f"Error uploading model to IPFS: {e}")
            raise
    
    async def download_model(self, cid: str, download_dir: Optional[Path] = None) -> Dict:
        """Download a model from IPFS"""
        if not self.client:
            raise ConnectionError("IPFS client not connected")
        
        try:
            download_dir = download_dir or self.models_dir
            download_path = download_dir / f"model_{cid}.zip"
            
            # Download from IPFS
            self.client.get(cid, target=str(download_dir))
            
            # Extract the package
            extracted_dir = download_dir / f"model_{cid}"
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_dir)
            
            # Load metadata
            metadata_path = extracted_dir / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {}
            
            logger.info(f"Model downloaded from IPFS: {cid}")
            return {
                'cid': cid,
                'download_path': str(extracted_dir),
                'metadata': metadata
            }
        
        except Exception as e:
            logger.error(f"Error downloading model from IPFS: {e}")
            raise
    
    async def upload_data(self, data_path: Path, data_info: Dict, node_id: str) -> Dict:
        """Upload training data to IPFS"""
        if not self.client:
            raise ConnectionError("IPFS client not connected")
        
        try:
            # Create a package with data and metadata
            package_path = await self._create_data_package(data_path, data_info)
            
            # Upload to IPFS
            result = self.client.add(str(package_path))
            cid = result['Hash']
            
            # Create metadata
            file_size = package_path.stat().st_size
            
            metadata = IPFSDataMetadata(
                data_id=data_info.get('data_id', 'unknown'),
                cid=cid,
                created_at=data_info.get('created_at', datetime.now().isoformat()),
                uploaded_at=datetime.now().isoformat(),
                file_size=file_size,
                data_type=data_info.get('data_type', 'unknown'),
                node_id=node_id,
                sample_count=data_info.get('sample_count'),
                features=data_info.get('features'),
                description=data_info.get('description')
            )
            
            # Save metadata
            self.data_metadata[cid] = asdict(metadata)
            self._save_metadata(self.data_metadata, self.data_metadata_file)
            
            # Clean up temporary package
            package_path.unlink()
            
            logger.info(f"Data uploaded to IPFS: {cid}")
            return {
                'cid': cid,
                'metadata': asdict(metadata),
                'ipfs_url': f'https://ipfs.io/ipfs/{cid}'
            }
        
        except Exception as e:
            logger.error(f"Error uploading data to IPFS: {e}")
            raise
    
    async def _create_model_package(self, model_path: Path, model_info: Dict) -> Path:
        """Create a ZIP package containing model and metadata"""
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
            package_path = Path(temp_file.name)
        
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add model file
            zip_file.write(model_path, model_path.name)
            
            # Add metadata
            metadata_content = json.dumps(model_info, indent=2, ensure_ascii=False)
            zip_file.writestr("metadata.json", metadata_content)
            
            # Add info file
            info_content = f"""
PeerAI Model Package
===================
Model ID: {model_info.get('model_id', 'N/A')}
Model Type: {model_info.get('type', 'N/A')}
Created: {model_info.get('created_at', 'N/A')}
Accuracy: {model_info.get('final_accuracy', 'N/A')}

This package was created by PeerAI IPFS integration system.
"""
            zip_file.writestr("README.txt", info_content)
        
        return package_path
    
    async def _create_data_package(self, data_path: Path, data_info: Dict) -> Path:
        """Create a ZIP package containing data and metadata"""
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
            package_path = Path(temp_file.name)
        
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add data file
            zip_file.write(data_path, data_path.name)
            
            # Add metadata
            metadata_content = json.dumps(data_info, indent=2, ensure_ascii=False)
            zip_file.writestr("metadata.json", metadata_content)
            
            # Add info file
            info_content = f"""
PeerAI Data Package
==================
Data ID: {data_info.get('data_id', 'N/A')}
Data Type: {data_info.get('data_type', 'N/A')}
Created: {data_info.get('created_at', 'N/A')}
Sample Count: {data_info.get('sample_count', 'N/A')}

This package was created by PeerAI IPFS integration system.
"""
            zip_file.writestr("README.txt", info_content)
        
        return package_path
    
    async def list_models(self) -> List[Dict]:
        """List all models in IPFS metadata"""
        return list(self.models_metadata.values())
    
    async def list_data(self) -> List[Dict]:
        """List all data in IPFS metadata"""
        return list(self.data_metadata.values())
    
    async def search_models(self, query: str) -> List[Dict]:
        """Search models by query"""
        results = []
        query_lower = query.lower()
        
        for metadata in self.models_metadata.values():
            if (query_lower in metadata.get('model_type', '').lower() or
                query_lower in metadata.get('description', '').lower() or
                query_lower in metadata.get('model_id', '').lower()):
                results.append(metadata)
        
        return results
    
    def get_ipfs_status(self) -> Dict:
        """Get IPFS node status"""
        if not self.client:
            return {'connected': False, 'error': 'IPFS client not connected'}
        
        try:
            version_info = self.client.version()
            peer_id = self.client.id()['ID']
            
            return {
                'connected': True,
                'version': version_info['Version'],
                'peer_id': peer_id,
                'models_count': len(self.models_metadata),
                'data_count': len(self.data_metadata)
            }
        except Exception as e:
            return {'connected': False, 'error': str(e)}
    
    async def pin_content(self, cid: str) -> bool:
        """Pin content to keep it available"""
        if not self.client:
            return False
        
        try:
            self.client.pin.add(cid)
            logger.info(f"Pinned content: {cid}")
            return True
        except Exception as e:
            logger.error(f"Error pinning content {cid}: {e}")
            return False
    
    async def unpin_content(self, cid: str) -> bool:
        """Unpin content to allow garbage collection"""
        if not self.client:
            return False
        
        try:
            self.client.pin.rm(cid)
            logger.info(f"Unpinned content: {cid}")
            return True
        except Exception as e:
            logger.error(f"Error unpinning content {cid}: {e}")
            return False
