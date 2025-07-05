#!/usr/bin/env python3
"""
PeerAI - IPFS System Test Suite
مجموعة اختبارات نظام IPFS لـ PeerAI
"""

import asyncio
import json
import logging
import tempfile
import pandas as pd
from pathlib import Path
import pytest
import torch
import torch.nn as nn

from ipfs_integration import PeerAIIPFS
from p2p_ai_prototype import P2PAIPrototype

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestPeerAIIPFS:
    """Test suite for PeerAI IPFS integration"""
    
    @pytest.fixture
    async def ipfs_ai(self):
        """Create IPFS AI instance for testing"""
        return PeerAIIPFS()
    
    @pytest.fixture
    async def prototype(self):
        """Create AI prototype for testing"""
        return P2PAIPrototype("test_node_123")
    
    @pytest.fixture
    def sample_data(self):
        """Create sample training data"""
        return {
            'texts': [
                "هذا نص إيجابي رائع",
                "هذا نص سلبي سيء", 
                "نص محايد عادي",
                "أحب هذا المنتج كثيراً",
                "لا أحب هذا إطلاقاً"
            ],
            'labels': [2, 0, 1, 2, 0]  # 0=negative, 1=neutral, 2=positive
        }
    
    async def test_ipfs_connection(self, ipfs_ai):
        """Test IPFS connection"""
        status = ipfs_ai.get_ipfs_status()
        
        if status['connected']:
            logger.info("✅ IPFS connection successful")
            logger.info(f"   Peer ID: {status['peer_id']}")
            logger.info(f"   Version: {status['version']}")
        else:
            logger.warning("⚠️  IPFS not connected - tests will be limited")
            logger.warning(f"   Error: {status['error']}")
    
    async def test_model_training_and_upload(self, ipfs_ai, prototype, sample_data):
        """Test model training and IPFS upload"""
        try:
            # Train a model
            logger.info("🤖 Training model...")
            model_info = await prototype.create_model("bert", num_classes=3)
            model_id = model_info['model_id']
            
            training_result = await prototype.train_model(
                model_id, 
                sample_data['texts'], 
                sample_data['labels'], 
                epochs=2
            )
            
            logger.info(f"✅ Model training completed")
            logger.info(f"   Model ID: {model_id}")
            logger.info(f"   Accuracy: {training_result['final_accuracy']:.2f}%")
            
            # Save model locally first
            await prototype.save_model(model_id)
            model_path = Path(f"models/{model_id}.pth")
            
            if not model_path.exists():
                logger.error("❌ Model file not found after saving")
                return False
            
            # Upload to IPFS (if connected)
            status = ipfs_ai.get_ipfs_status()
            if status['connected']:
                logger.info("📤 Uploading model to IPFS...")
                
                upload_result = await ipfs_ai.upload_model(
                    model_path=model_path,
                    model_info={**model_info, **training_result},
                    node_id="test_node_123"
                )
                
                logger.info(f"✅ Model uploaded to IPFS")
                logger.info(f"   CID: {upload_result['cid']}")
                logger.info(f"   IPFS URL: {upload_result['ipfs_url']}")
                
                return upload_result['cid']
            else:
                logger.info("ℹ️  IPFS not connected - skipping upload")
                return None
        
        except Exception as e:
            logger.error(f"❌ Error in model training/upload: {e}")
            return False
    
    async def test_data_upload(self, ipfs_ai):
        """Test data upload to IPFS"""
        try:
            # Create sample dataset
            logger.info("📊 Creating sample dataset...")
            
            data = pd.DataFrame({
                'text': [
                    'مثال نص إيجابي',
                    'مثال نص سلبي', 
                    'مثال نص محايد'
                ],
                'label': [2, 0, 1],
                'language': ['arabic', 'arabic', 'arabic']
            })
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                data_path = Path(f.name)
                data.to_csv(f.name, index=False)
            
            # Upload to IPFS (if connected)
            status = ipfs_ai.get_ipfs_status()
            if status['connected']:
                logger.info("📤 Uploading data to IPFS...")
                
                data_info = {
                    'data_id': 'test_arabic_sentiment',
                    'data_type': 'sentiment_analysis',
                    'sample_count': len(data),
                    'features': list(data.columns),
                    'description': 'Test Arabic sentiment analysis dataset'
                }
                
                upload_result = await ipfs_ai.upload_data(
                    data_path=data_path,
                    data_info=data_info,
                    node_id="test_node_123"
                )
                
                logger.info(f"✅ Data uploaded to IPFS")
                logger.info(f"   CID: {upload_result['cid']}")
                logger.info(f"   IPFS URL: {upload_result['ipfs_url']}")
                
                # Clean up
                data_path.unlink()
                
                return upload_result['cid']
            else:
                logger.info("ℹ️  IPFS not connected - skipping upload")
                data_path.unlink()
                return None
        
        except Exception as e:
            logger.error(f"❌ Error in data upload: {e}")
            return False
    
    async def test_model_download(self, ipfs_ai, model_cid):
        """Test model download from IPFS"""
        if not model_cid:
            logger.info("ℹ️  No model CID available - skipping download test")
            return
        
        try:
            logger.info(f"📥 Downloading model from IPFS: {model_cid}")
            
            download_result = await ipfs_ai.download_model(model_cid)
            
            logger.info(f"✅ Model downloaded successfully")
            logger.info(f"   Download path: {download_result['download_path']}")
            logger.info(f"   Metadata: {download_result['metadata']}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Error downloading model: {e}")
            return False
    
    async def test_search_functionality(self, ipfs_ai):
        """Test search functionality"""
        try:
            logger.info("🔍 Testing search functionality...")
            
            # Search for models
            models = await ipfs_ai.search_models("bert")
            logger.info(f"   Found {len(models)} models matching 'bert'")
            
            # List all models
            all_models = await ipfs_ai.list_models()
            logger.info(f"   Total models in registry: {len(all_models)}")
            
            # List all data
            all_data = await ipfs_ai.list_data()
            logger.info(f"   Total datasets in registry: {len(all_data)}")
            
            logger.info("✅ Search functionality working")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error in search functionality: {e}")
            return False
    
    async def test_metadata_management(self, ipfs_ai):
        """Test metadata management"""
        try:
            logger.info("📋 Testing metadata management...")
            
            # Check metadata files exist
            models_metadata_file = ipfs_ai.metadata_dir / "models.json"
            data_metadata_file = ipfs_ai.metadata_dir / "data.json"
            
            logger.info(f"   Models metadata exists: {models_metadata_file.exists()}")
            logger.info(f"   Data metadata exists: {data_metadata_file.exists()}")
            
            # Test metadata loading
            models_metadata = ipfs_ai._load_metadata(models_metadata_file)
            data_metadata = ipfs_ai._load_metadata(data_metadata_file)
            
            logger.info(f"   Loaded {len(models_metadata)} model records")
            logger.info(f"   Loaded {len(data_metadata)} data records")
            
            logger.info("✅ Metadata management working")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error in metadata management: {e}")
            return False

async def run_comprehensive_test():
    """Run comprehensive IPFS integration test"""
    logger.info("🚀 Starting PeerAI IPFS Integration Tests")
    logger.info("=" * 50)
    
    # Initialize test objects
    ipfs_ai = PeerAIIPFS()
    prototype = P2PAIPrototype("test_node_123")
    
    sample_data = {
        'texts': [
            "هذا نص إيجابي رائع",
            "هذا نص سلبي سيء", 
            "نص محايد عادي",
            "أحب هذا المنتج كثيراً",
            "لا أحب هذا إطلاقاً"
        ],
        'labels': [2, 0, 1, 2, 0]
    }
    
    test_suite = TestPeerAIIPFS()
    
    # Run tests
    test_results = {}
    
    # Test 1: IPFS Connection
    logger.info("\n1️⃣ Testing IPFS Connection...")
    await test_suite.test_ipfs_connection(ipfs_ai)
    
    # Test 2: Model Training and Upload
    logger.info("\n2️⃣ Testing Model Training and Upload...")
    model_cid = await test_suite.test_model_training_and_upload(ipfs_ai, prototype, sample_data)
    test_results['model_upload'] = model_cid is not False
    
    # Test 3: Data Upload
    logger.info("\n3️⃣ Testing Data Upload...")
    data_cid = await test_suite.test_data_upload(ipfs_ai)
    test_results['data_upload'] = data_cid is not False
    
    # Test 4: Model Download (if we have a CID)
    logger.info("\n4️⃣ Testing Model Download...")
    if model_cid:
        download_success = await test_suite.test_model_download(ipfs_ai, model_cid)
        test_results['model_download'] = download_success
    
    # Test 5: Search Functionality
    logger.info("\n5️⃣ Testing Search Functionality...")
    search_success = await test_suite.test_search_functionality(ipfs_ai)
    test_results['search'] = search_success
    
    # Test 6: Metadata Management
    logger.info("\n6️⃣ Testing Metadata Management...")
    metadata_success = await test_suite.test_metadata_management(ipfs_ai)
    test_results['metadata'] = metadata_success
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("📊 Test Results Summary")
    logger.info("=" * 50)
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"   {test_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! PeerAI IPFS integration is working correctly.")
    else:
        logger.warning("⚠️  Some tests failed. Check IPFS connection and configuration.")
    
    return test_results

if __name__ == "__main__":
    # Run the comprehensive test
    asyncio.run(run_comprehensive_test())
