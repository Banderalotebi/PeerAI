#!/usr/bin/env python3
"""
PeerAI - IPFS Training and Sharing System
نظام التدريب والمشاركة على IPFS لـ PeerAI
"""

import asyncio
import json
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from p2p_ai_prototype import P2PAIPrototype
from ipfs_integration import PeerAIIPFS
from p2p_identity_system import P2PIdentityManager
from p2p_rewards_system import P2PRewardsSystem

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PeerAIIPFSTrainer:
    """Main class for PeerAI IPFS training and sharing"""
    
    def __init__(self, node_id: Optional[str] = None):
        """Initialize the trainer"""
        # Initialize systems
        self.identity_manager = P2PIdentityManager()
        self.node_id = node_id or self.identity_manager.own_keys['node_id']
        
        self.prototype = P2PAIPrototype(self.node_id)
        self.ipfs_ai = PeerAIIPFS()
        self.rewards_system = P2PRewardsSystem()
        
        logger.info(f"🚀 PeerAI IPFS Trainer initialized for node: {self.node_id}")
    
    async def create_and_train_model(self, 
                                   model_type: str = "bert",
                                   texts: List[str] = None,
                                   labels: List[int] = None,
                                   epochs: int = 3,
                                   description: str = None) -> Dict:
        """Create, train, and prepare a model for sharing"""
        try:
            # Use sample data if none provided
            if texts is None or labels is None:
                texts, labels = self._get_sample_arabic_data()
            
            logger.info(f"🤖 Creating {model_type} model...")
            
            # Create model
            model_info = await self.prototype.create_model(
                model_type, 
                num_classes=len(set(labels))
            )
            model_id = model_info['model_id']
            
            logger.info(f"✅ Model created: {model_id}")
            
            # Train model
            logger.info(f"🎯 Training model with {len(texts)} samples for {epochs} epochs...")
            training_result = await self.prototype.train_model(
                model_id, texts, labels, epochs=epochs
            )
            
            logger.info(f"✅ Training completed - Accuracy: {training_result['final_accuracy']:.2f}%")
            
            # Add description and metadata
            model_info.update(training_result)
            model_info['description'] = description or f"Arabic {model_type} model trained on {len(texts)} samples"
            model_info['training_samples'] = len(texts)
            model_info['node_id'] = self.node_id
            
            return model_info
        
        except Exception as e:
            logger.error(f"❌ Error in model creation/training: {e}")
            raise
    
    async def share_model_to_ipfs(self, model_info: Dict) -> Dict:
        """Share a trained model to IPFS"""
        try:
            model_id = model_info['model_id']
            
            # Check IPFS connection
            status = self.ipfs_ai.get_ipfs_status()
            if not status['connected']:
                raise ConnectionError("IPFS not connected. Please start IPFS daemon.")
            
            logger.info(f"📤 Uploading model {model_id} to IPFS...")
            
            # Ensure model is saved locally
            await self.prototype.save_model(model_id)
            model_path = Path(f"models/{model_id}.pth")
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            # Upload to IPFS
            upload_result = await self.ipfs_ai.upload_model(
                model_path=model_path,
                model_info=model_info,
                node_id=self.node_id
            )
            
            logger.info(f"✅ Model uploaded to IPFS")
            logger.info(f"   CID: {upload_result['cid']}")
            logger.info(f"   IPFS URL: {upload_result['ipfs_url']}")
            
            # Award rewards for model sharing
            await self._award_sharing_rewards(upload_result['cid'], 'model_training')
            
            return upload_result
        
        except Exception as e:
            logger.error(f"❌ Error sharing model to IPFS: {e}")
            raise
    
    async def share_data_to_ipfs(self, data_path: Path, data_info: Dict) -> Dict:
        """Share training data to IPFS"""
        try:
            # Check IPFS connection
            status = self.ipfs_ai.get_ipfs_status()
            if not status['connected']:
                raise ConnectionError("IPFS not connected. Please start IPFS daemon.")
            
            logger.info(f"📤 Uploading data to IPFS...")
            
            # Upload to IPFS
            upload_result = await self.ipfs_ai.upload_data(
                data_path=data_path,
                data_info=data_info,
                node_id=self.node_id
            )
            
            logger.info(f"✅ Data uploaded to IPFS")
            logger.info(f"   CID: {upload_result['cid']}")
            logger.info(f"   IPFS URL: {upload_result['ipfs_url']}")
            
            # Award rewards for data sharing
            await self._award_sharing_rewards(upload_result['cid'], 'data_contribution')
            
            return upload_result
        
        except Exception as e:
            logger.error(f"❌ Error sharing data to IPFS: {e}")
            raise
    
    async def download_and_use_model(self, cid: str) -> Dict:
        """Download a model from IPFS and load it"""
        try:
            logger.info(f"📥 Downloading model from IPFS: {cid}")
            
            # Download from IPFS
            download_result = await self.ipfs_ai.download_model(cid)
            
            logger.info(f"✅ Model downloaded successfully")
            
            # Load the model (this would require extending the prototype)
            # For now, just return the download info
            return download_result
        
        except Exception as e:
            logger.error(f"❌ Error downloading model: {e}")
            raise
    
    async def discover_models(self, query: Optional[str] = None) -> List[Dict]:
        """Discover available models on the network"""
        try:
            logger.info("🔍 Discovering available models...")
            
            if query:
                models = await self.ipfs_ai.search_models(query)
                logger.info(f"   Found {len(models)} models matching '{query}'")
            else:
                models = await self.ipfs_ai.list_models()
                logger.info(f"   Found {len(models)} total models")
            
            # Display models
            for i, model in enumerate(models[:5]):  # Show top 5
                logger.info(f"   {i+1}. {model.get('model_id', 'Unknown')} - "
                          f"CID: {model.get('cid', 'Unknown')[:16]}... - "
                          f"Accuracy: {model.get('accuracy', 'N/A')}")
            
            return models
        
        except Exception as e:
            logger.error(f"❌ Error discovering models: {e}")
            return []
    
    async def collaborative_training(self, base_cid: Optional[str] = None) -> Dict:
        """Perform collaborative training using shared models/data"""
        try:
            logger.info("🤝 Starting collaborative training...")
            
            # Download base model if provided
            if base_cid:
                logger.info(f"📥 Using base model: {base_cid}")
                base_model = await self.download_and_use_model(base_cid)
            
            # Get local data
            texts, labels = self._get_sample_arabic_data()
            
            # Train improved model
            model_info = await self.create_and_train_model(
                texts=texts,
                labels=labels,
                epochs=5,
                description=f"Collaborative training{'based on ' + base_cid[:16] + '...' if base_cid else ''}"
            )
            
            # Share the improved model
            upload_result = await self.share_model_to_ipfs(model_info)
            
            logger.info("✅ Collaborative training completed and shared!")
            return upload_result
        
        except Exception as e:
            logger.error(f"❌ Error in collaborative training: {e}")
            raise
    
    async def _award_sharing_rewards(self, cid: str, contribution_type: str):
        """Award rewards for sharing content"""
        try:
            # Calculate reward based on contribution type
            base_reward = {
                'data_contribution': 5.0,
                'model_training': 10.0,
                'knowledge_extraction': 15.0
            }.get(contribution_type, 5.0)
            
            # Add contribution record
            contribution = await self.rewards_system.add_contribution(
                node_id=self.node_id,
                contribution_type=contribution_type,
                data_hash=cid,
                quality_score=0.8,  # Default quality score
                metadata={'ipfs_cid': cid}
            )
            
            logger.info(f"💰 Awarded {base_reward} tokens for {contribution_type}")
            
        except Exception as e:
            logger.warning(f"⚠️  Could not award rewards: {e}")
    
    def _get_sample_arabic_data(self) -> tuple:
        """Get sample Arabic training data"""
        texts = [
            "هذا منتج رائع وأنصح بشرائه",
            "المنتج سيء جداً ولا أنصح به",
            "المنتج مقبول وليس سيء",
            "أحببت هذا المنتج كثيراً",
            "المنتج فشل توقعاتي تماماً",
            "جودة المنتج متوسطة",
            "هذا أفضل منتج اشتريته",
            "المنتج لا يستحق السعر",
            "منتج عادي لا أكثر",
            "استمتعت باستخدام هذا المنتج"
        ]
        
        # Labels: 0=negative, 1=neutral, 2=positive
        labels = [2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
        
        return texts, labels
    
    async def get_status(self) -> Dict:
        """Get system status"""
        ipfs_status = self.ipfs_ai.get_ipfs_status()
        models = await self.ipfs_ai.list_models()
        data = await self.ipfs_ai.list_data()
        
        return {
            'node_id': self.node_id,
            'ipfs_connected': ipfs_status['connected'],
            'ipfs_peer_id': ipfs_status.get('peer_id', 'N/A'),
            'local_models': len(self.prototype.models),
            'shared_models': len(models),
            'shared_datasets': len(data),
            'reputation': self.rewards_system.get_reputation(self.node_id)
        }

async def main():
    """Main demonstration of PeerAI IPFS training and sharing"""
    print("🌐 PeerAI IPFS Training and Sharing System")
    print("=" * 50)
    
    try:
        # Initialize trainer
        trainer = PeerAIIPFSTrainer()
        
        # Check status
        status = await trainer.get_status()
        print(f"📊 System Status:")
        print(f"   Node ID: {status['node_id']}")
        print(f"   IPFS Connected: {status['ipfs_connected']}")
        print(f"   Local Models: {status['local_models']}")
        print(f"   Shared Models: {status['shared_models']}")
        
        if not status['ipfs_connected']:
            print("\n⚠️  IPFS not connected. Please start IPFS daemon:")
            print("   $ ipfs daemon")
            return
        
        # Create and train a model
        print(f"\n🤖 Creating and training Arabic sentiment model...")
        model_info = await trainer.create_and_train_model(
            model_type="bert",
            epochs=3,
            description="Arabic sentiment analysis model for product reviews"
        )
        
        # Share to IPFS
        print(f"\n📤 Sharing model to IPFS...")
        upload_result = await trainer.share_model_to_ipfs(model_info)
        
        # Discover other models
        print(f"\n🔍 Discovering other models on the network...")
        models = await trainer.discover_models("sentiment")
        
        # Create and share sample data
        print(f"\n📊 Creating and sharing sample dataset...")
        
        # Create sample CSV data
        texts, labels = trainer._get_sample_arabic_data()
        sample_data = pd.DataFrame({
            'text': texts,
            'label': labels,
            'language': ['arabic'] * len(texts)
        })
        
        data_path = Path("sample_arabic_sentiment.csv")
        sample_data.to_csv(data_path, index=False)
        
        data_info = {
            'data_id': 'arabic_sentiment_sample',
            'data_type': 'sentiment_analysis',
            'sample_count': len(sample_data),
            'features': list(sample_data.columns),
            'description': 'Sample Arabic sentiment analysis dataset for product reviews'
        }
        
        data_upload = await trainer.share_data_to_ipfs(data_path, data_info)
        
        print(f"\n🎉 Demo completed successfully!")
        print(f"   Model CID: {upload_result['cid']}")
        print(f"   Data CID: {data_upload['cid']}")
        print(f"   Check your models at: https://ipfs.io/ipfs/{upload_result['cid']}")
        
        # Clean up
        data_path.unlink()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\nTroubleshooting:")
        print(f"1. Make sure IPFS is installed and running: $ ipfs daemon")
        print(f"2. Install dependencies: $ pip install -r requirements_ipfs.txt")
        print(f"3. Check IPFS connection: $ ipfs id")

if __name__ == "__main__":
    print("PeerAI IPFS Training System - Ready!")
    asyncio.run(main())
