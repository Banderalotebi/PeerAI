#!/usr/bin/env python3
"""
P2P Identity System - Simplified Version
نظام الهوية اللامركزي - نسخة مبسطة
"""

import json
import hashlib
import secrets
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Identity:
    """Node identity information"""
    node_id: str
    public_key: str
    created_at: str
    last_seen: str
    reputation: float = 0.0
    contributions: int = 0
    verified: bool = False

@dataclass
class Signature:
    """Digital signature information"""
    node_id: str
    data_hash: str
    signature: str
    timestamp: str
    algorithm: str = "sha256"

class P2PIdentityManager:
    """Manages node identities and signatures"""
    
    def __init__(self, config_dir: str = ".p2p_identity"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.identities_file = self.config_dir / "identities.json"
        self.keys_file = self.config_dir / "keys.json"
        
        # Load or create identity database
        self.identities = self._load_identities()
        
        # Generate or load own keys
        self.own_keys = self._load_or_generate_keys()
        
        logger.info(f"Identity manager initialized for node: {self.own_keys['node_id']}")
    
    def _load_identities(self):
        """Load identities from file"""
        if self.identities_file.exists():
            with open(self.identities_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {node_id: Identity(**identity_data) for node_id, identity_data in data.items()}
        return {}
    
    def _save_identities(self):
        """Save identities to file"""
        data = {node_id: {
            'node_id': identity.node_id,
            'public_key': identity.public_key,
            'created_at': identity.created_at,
            'last_seen': identity.last_seen,
            'reputation': identity.reputation,
            'contributions': identity.contributions,
            'verified': identity.verified
        } for node_id, identity in self.identities.items()}
        
        with open(self.identities_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_or_generate_keys(self):
        """Load existing keys or generate new ones"""
        if self.keys_file.exists():
            with open(self.keys_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Generate new keys
        node_id = f"node_{secrets.token_hex(8)}"
        private_key = secrets.token_hex(32)
        public_key = hashlib.sha256(private_key.encode()).hexdigest()
        
        keys = {
            "node_id": node_id,
            "private_key": private_key,
            "public_key": public_key,
            "created_at": datetime.now().isoformat()
        }
        
        # Save keys
        with open(self.keys_file, 'w', encoding='utf-8') as f:
            json.dump(keys, f, indent=2)
        
        # Add own identity
        self.identities[node_id] = Identity(
            node_id=node_id,
            public_key=keys["public_key"],
            created_at=keys["created_at"],
            last_seen=datetime.now().isoformat(),
            verified=True
        )
        self._save_identities()
        
        return keys
    
    def get_node_id(self):
        """Get own node ID"""
        return self.own_keys["node_id"]
    
    def get_public_key(self):
        """Get own public key"""
        return self.own_keys["public_key"]
    
    def create_signature(self, data: str):
        """Create a digital signature for data"""
        node_id = self.get_node_id()
        timestamp = datetime.now().isoformat()
        
        # Create data hash
        data_to_hash = f"{data}:{timestamp}:{node_id}"
        data_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
        
        # Create signature using HMAC
        signature_data = f"{data_hash}:{timestamp}:{node_id}"
        signature = hashlib.sha256(
            self.own_keys["private_key"].encode() + signature_data.encode()
        ).hexdigest()
        
        return Signature(
            node_id=node_id,
            data_hash=data_hash,
            signature=signature,
            timestamp=timestamp,
            algorithm="hmac-sha256"
        )
    
    def verify_signature(self, data: str, signature):
        """Verify a digital signature"""
        try:
            # Recreate data hash
            data_to_hash = f"{data}:{signature.timestamp}:{signature.node_id}"
            expected_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
            
            if expected_hash != signature.data_hash:
                return False
            
            # Get signer's public key
            if signature.node_id not in self.identities:
                logger.warning(f"Unknown node ID: {signature.node_id}")
                return False
            
            public_key_data = self.identities[signature.node_id].public_key
            
            # Verify HMAC signature
            signature_data = f"{signature.data_hash}:{signature.timestamp}:{signature.node_id}"
            expected_signature = hashlib.sha256(
                public_key_data.encode() + signature_data.encode()
            ).hexdigest()
            
            return signature.signature == expected_signature
        
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            return False
    
    def add_identity(self, node_id: str, public_key: str, verified: bool = False):
        """Add a new node identity"""
        try:
            if node_id in self.identities:
                # Update existing identity
                self.identities[node_id].last_seen = datetime.now().isoformat()
                self.identities[node_id].public_key = public_key
                if verified:
                    self.identities[node_id].verified = True
            else:
                # Create new identity
                self.identities[node_id] = Identity(
                    node_id=node_id,
                    public_key=public_key,
                    created_at=datetime.now().isoformat(),
                    last_seen=datetime.now().isoformat(),
                    verified=verified
                )
            
            self._save_identities()
            logger.info(f"Added/updated identity: {node_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error adding identity: {e}")
            return False
    
    def update_reputation(self, node_id: str, reputation_change: float):
        """Update node reputation"""
        if node_id not in self.identities:
            return False
        
        self.identities[node_id].reputation += reputation_change
        self.identities[node_id].contributions += 1
        self.identities[node_id].last_seen = datetime.now().isoformat()
        
        self._save_identities()
        logger.info(f"Updated reputation for {node_id}: {reputation_change}")
        return True
    
    def get_trusted_nodes(self, min_reputation: float = 0.0):
        """Get list of trusted nodes"""
        trusted = []
        for node_id, identity in self.identities.items():
            if identity.verified and identity.reputation >= min_reputation:
                trusted.append(node_id)
        
        return sorted(trusted, key=lambda x: self.identities[x].reputation, reverse=True)
    
    def export_identity(self):
        """Export own identity for sharing"""
        return {
            'node_id': self.get_node_id(),
            'public_key': self.get_public_key(),
            'created_at': self.own_keys['created_at'],
            'verified': True
        }

# Example usage and testing
def main():
    """Test the identity and signature system"""
    print("🔐 Testing P2P Identity and Signature System...")
    
    # Create identity manager
    identity_manager = P2PIdentityManager()
    
    print(f"✅ Node ID: {identity_manager.get_node_id()}")
    print(f"✅ Public Key: {identity_manager.get_public_key()[:50]}...")
    
    # Test signature creation and verification
    test_data = "Hello, P2P AI Network! مرحباً بشبكة الذكاء الاصطناعي اللامركزية!"
    
    print(f"\n📝 Creating signature for: {test_data}")
    signature = identity_manager.create_signature(test_data)
    print(f"✅ Signature created: {signature.signature[:50]}...")
    
    # Verify signature
    is_valid = identity_manager.verify_signature(test_data, signature)
    print(f"✅ Signature verification: {'PASS' if is_valid else 'FAIL'}")
    
    # Test with invalid data
    is_valid_invalid = identity_manager.verify_signature("Invalid data", signature)
    print(f"✅ Invalid data verification: {'PASS' if not is_valid_invalid else 'FAIL'}")
    
    # Add another identity
    other_node_id = "node_456"
    other_public_key = "other_public_key_123"
    identity_manager.add_identity(other_node_id, other_public_key)
    
    # Update reputation
    identity_manager.update_reputation(other_node_id, 10.0)
    
    # Get trusted nodes
    trusted_nodes = identity_manager.get_trusted_nodes()
    print(f"\n🤝 Trusted nodes: {trusted_nodes}")
    
    # Export and import identity
    exported_identity = identity_manager.export_identity()
    print(f"\n📤 Exported identity: {exported_identity}")
    
    print("\n🎉 Identity system test completed!")

if __name__ == "__main__":
    main()
