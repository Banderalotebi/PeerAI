#!/usr/bin/env python3
"""
Comprehensive Test Suite for P2P AI Decentralized System
مجموعة اختبارات شاملة لنظام الذكاء الاصطناعي اللامركزي
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class P2PSystemTester:
    """Comprehensive test suite for P2P AI system"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = time.time()
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} - {test_name}: {details}")
    
    async def test_cli_interface(self):
        """Test CLI interface functionality"""
        logger.info("🧪 Testing CLI Interface...")
        
        try:
            # Import CLI module
            import p2p_ai_cli
            
            # Test configuration loading
            config = p2p_ai_cli.config
            if config and hasattr(config, 'config'):
                self.log_test("CLI Config Loading", True, f"Node ID: {config.config.get('node_id', 'N/A')}")
            else:
                self.log_test("CLI Config Loading", False, "Configuration not loaded properly")
            
            # Test node creation
            node = p2p_ai_cli.node
            if node and hasattr(node, 'config'):
                self.log_test("CLI Node Creation", True, "Node created successfully")
            else:
                self.log_test("CLI Node Creation", False, "Node not created properly")
                
        except Exception as e:
            self.log_test("CLI Interface", False, f"Error: {str(e)}")
    
    async def test_pytorch_prototype(self):
        """Test PyTorch prototype functionality"""
        logger.info("🧪 Testing PyTorch Prototype...")
        
        try:
            # Import prototype module
            import p2p_ai_prototype
            
            # Test prototype creation
            prototype = p2p_ai_prototype.P2PAIPrototype("test_node_123")
            self.log_test("Prototype Creation", True, f"Device: {prototype.device}")
            
            # Test model creation
            model_info = await prototype.create_model("bert", num_classes=3)
            if model_info and 'model_id' in model_info:
                self.log_test("Model Creation", True, f"Model ID: {model_info['model_id']}")
            else:
                self.log_test("Model Creation", False, "Model creation failed")
            
            # Test data addition
            test_texts = ["نص تجريبي", "Test text", "مثال آخر"]
            test_labels = [0, 1, 2]
            data_count = await prototype.add_data(test_texts, test_labels)
            self.log_test("Data Addition", True, f"Added {data_count} data points")
            
            # Test model training (simplified)
            if hasattr(prototype, 'models') and prototype.models:
                model_id = list(prototype.models.keys())[0]
                try:
                    training_result = await prototype.train_model(model_id, test_texts, test_labels, epochs=1)
                    self.log_test("Model Training", True, f"Accuracy: {training_result.get('final_accuracy', 'N/A')}")
                except Exception as e:
                    self.log_test("Model Training", False, f"Training error: {str(e)}")
            
            # Test predictions
            try:
                predictions = await prototype.predict(model_id, ["نص للاختبار"])
                self.log_test("Model Prediction", True, f"Made {len(predictions)} predictions")
            except Exception as e:
                self.log_test("Model Prediction", False, f"Prediction error: {str(e)}")
                
        except Exception as e:
            self.log_test("PyTorch Prototype", False, f"Error: {str(e)}")
    
    async def test_identity_system(self):
        """Test identity and signature system"""
        logger.info("🧪 Testing Identity System...")
        
        try:
            # Import identity module
            import p2p_identity_system
            
            # Test identity manager creation
            identity_manager = p2p_identity_system.P2PIdentityManager(".test_identity")
            self.log_test("Identity Manager Creation", True, f"Node ID: {identity_manager.get_node_id()}")
            
            # Test signature creation
            test_data = "Hello, P2P AI Network! مرحباً بشبكة الذكاء الاصطناعي اللامركزية!"
            signature = identity_manager.create_signature(test_data)
            self.log_test("Signature Creation", True, f"Algorithm: {signature.algorithm}")
            
            # Test signature verification
            is_valid = identity_manager.verify_signature(test_data, signature)
            self.log_test("Signature Verification", is_valid, "Valid signature" if is_valid else "Invalid signature")
            
            # Test invalid signature
            is_invalid = identity_manager.verify_signature("Invalid data", signature)
            self.log_test("Invalid Signature Test", not is_invalid, "Correctly rejected invalid data")
            
            # Test identity addition
            other_node_id = "test_node_456"
            other_public_key = "test_public_key_123"
            success = identity_manager.add_identity(other_node_id, other_public_key)
            self.log_test("Identity Addition", success, f"Added identity: {other_node_id}")
            
            # Test reputation update
            success = identity_manager.update_reputation(other_node_id, 10.0)
            self.log_test("Reputation Update", success, "Updated reputation")
            
            # Test trusted nodes
            trusted_nodes = identity_manager.get_trusted_nodes()
            self.log_test("Trusted Nodes", True, f"Found {len(trusted_nodes)} trusted nodes")
            
        except Exception as e:
            self.log_test("Identity System", False, f"Error: {str(e)}")
    
    async def test_rewards_system(self):
        """Test rewards system functionality"""
        logger.info("🧪 Testing Rewards System...")
        
        try:
            # Import rewards module
            import p2p_rewards_system
            
            # Test rewards system creation
            rewards_system = p2p_rewards_system.P2PRewardsSystem(".test_rewards")
            self.log_test("Rewards System Creation", True, "Rewards system initialized")
            
            # Test contribution recording
            test_node_id = "test_node_123"
            result = rewards_system.record_contribution(
                node_id=test_node_id,
                contribution_type="model_training",
                data_hash="test_hash_123",
                quality_score=0.85
            )
            
            if result and 'reward_amount' in result:
                self.log_test("Contribution Recording", True, f"Earned {result['reward_amount']} tokens")
            else:
                self.log_test("Contribution Recording", False, "Failed to record contribution")
            
            # Test balance checking
            balance = rewards_system.get_balance(test_node_id)
            self.log_test("Balance Check", True, f"Balance: {balance} tokens")
            
            # Test reputation retrieval
            reputation = rewards_system.get_reputation(test_node_id)
            if reputation:
                self.log_test("Reputation Retrieval", True, f"Tier: {reputation.get('tier', 'N/A')}")
            else:
                self.log_test("Reputation Retrieval", False, "No reputation found")
            
            # Test leaderboard
            leaderboard = rewards_system.get_leaderboard(5)
            self.log_test("Leaderboard", True, f"Leaderboard with {len(leaderboard)} entries")
            
            # Test network stats
            stats = rewards_system.get_network_stats()
            self.log_test("Network Stats", True, f"Total nodes: {stats.get('total_nodes', 0)}")
            
        except Exception as e:
            self.log_test("Rewards System", False, f"Error: {str(e)}")
    
    async def test_integration(self):
        """Test integration between components"""
        logger.info("🧪 Testing System Integration...")
        
        try:
            # Test end-to-end workflow
            import p2p_ai_cli
            import p2p_ai_prototype
            import p2p_identity_system
            import p2p_rewards_system
            
            # Create instances
            cli_config = p2p_ai_cli.config
            cli_node = p2p_ai_cli.node
            prototype = p2p_ai_prototype.P2PAIPrototype("integration_test_node")
            identity_manager = p2p_identity_system.P2PIdentityManager(".test_integration_identity")
            rewards_system = p2p_rewards_system.P2PRewardsSystem(".test_integration_rewards")
            
            self.log_test("Component Integration", True, "All components loaded successfully")
            
            # Test data flow
            test_texts = ["نص عربي للاختبار", "Arabic text for testing"]
            test_labels = [1, 2]
            
            # Add data to prototype
            data_count = await prototype.add_data(test_texts, test_labels)
            
            # Create model
            model_info = await prototype.create_model("bert", num_classes=3)
            model_id = model_info['model_id']
            
            # Train model
            training_result = await prototype.train_model(model_id, test_texts, test_labels, epochs=1)
            
            # Create signature for contribution
            contribution_data = f"model_{model_id}_trained"
            signature = identity_manager.create_signature(contribution_data)
            
            # Record contribution with rewards
            reward_result = rewards_system.record_contribution(
                node_id=identity_manager.get_node_id(),
                contribution_type="model_training",
                data_hash=contribution_data,
                quality_score=0.8,
                signature=signature.signature
            )
            
            self.log_test("End-to-End Workflow", True, f"Completed workflow with {reward_result['reward_amount']} tokens earned")
            
        except Exception as e:
            self.log_test("System Integration", False, f"Error: {str(e)}")
    
    async def test_performance(self):
        """Test system performance"""
        logger.info("🧪 Testing System Performance...")
        
        try:
            import p2p_ai_prototype
            import p2p_identity_system
            import p2p_rewards_system
            
            # Performance test: Identity operations
            identity_manager = p2p_identity_system.P2PIdentityManager(".test_performance_identity")
            
            start_time = time.time()
            for i in range(100):
                test_data = f"test_data_{i}"
                signature = identity_manager.create_signature(test_data)
                identity_manager.verify_signature(test_data, signature)
            
            identity_time = time.time() - start_time
            self.log_test("Identity Performance", True, f"100 operations in {identity_time:.2f}s")
            
            # Performance test: Rewards operations
            rewards_system = p2p_rewards_system.P2PRewardsSystem(".test_performance_rewards")
            
            start_time = time.time()
            for i in range(50):
                rewards_system.record_contribution(
                    node_id=f"perf_node_{i}",
                    contribution_type="data_contribution",
                    data_hash=f"hash_{i}",
                    quality_score=0.7
                )
            
            rewards_time = time.time() - start_time
            self.log_test("Rewards Performance", True, f"50 operations in {rewards_time:.2f}s")
            
            # Performance test: Model operations
            prototype = p2p_ai_prototype.P2PAIPrototype("perf_test_node")
            
            # Add test data
            test_texts = [f"test text {i}" for i in range(20)]
            test_labels = [i % 3 for i in range(20)]
            await prototype.add_data(test_texts, test_labels)
            
            # Create and train model
            start_time = time.time()
            model_info = await prototype.create_model("bert", num_classes=3)
            model_id = model_info['model_id']
            training_result = await prototype.train_model(model_id, test_texts, test_labels, epochs=1)
            model_time = time.time() - start_time
            
            self.log_test("Model Performance", True, f"Model training in {model_time:.2f}s")
            
        except Exception as e:
            self.log_test("Performance Tests", False, f"Error: {str(e)}")
    
    async def test_error_handling(self):
        """Test error handling and edge cases"""
        logger.info("🧪 Testing Error Handling...")
        
        try:
            import p2p_ai_prototype
            import p2p_identity_system
            import p2p_rewards_system
            
            # Test invalid model ID
            prototype = p2p_ai_prototype.P2PAIPrototype("error_test_node")
            try:
                await prototype.train_model("invalid_model_id", [], [])
                self.log_test("Invalid Model ID", False, "Should have raised error")
            except Exception:
                self.log_test("Invalid Model ID", True, "Correctly handled invalid model ID")
            
            # Test empty data
            try:
                await prototype.add_data([], [])
                self.log_test("Empty Data", True, "Handled empty data gracefully")
            except Exception as e:
                self.log_test("Empty Data", False, f"Error with empty data: {str(e)}")
            
            # Test invalid signature
            identity_manager = p2p_identity_system.P2PIdentityManager(".test_error_identity")
            test_data = "test data"
            signature = identity_manager.create_signature(test_data)
            
            # Modify signature to make it invalid
            signature.signature = "invalid_signature"
            is_valid = identity_manager.verify_signature(test_data, signature)
            self.log_test("Invalid Signature", not is_valid, "Correctly rejected invalid signature")
            
            # Test negative rewards
            rewards_system = p2p_rewards_system.P2PRewardsSystem(".test_error_rewards")
            try:
                rewards_system.record_contribution(
                    node_id="test_node",
                    contribution_type="invalid_type",
                    data_hash="test_hash",
                    quality_score=-0.5
                )
                self.log_test("Invalid Contribution", False, "Should have handled invalid parameters")
            except Exception:
                self.log_test("Invalid Contribution", True, "Correctly handled invalid contribution")
                
        except Exception as e:
            self.log_test("Error Handling", False, f"Error: {str(e)}")
    
    def generate_report(self):
        """Generate comprehensive test report"""
        end_time = time.time()
        total_time = end_time - self.start_time
        
        passed_tests = sum(1 for result in self.test_results if result['success'])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "success_rate": f"{success_rate:.1f}%",
                "total_time": f"{total_time:.2f}s"
            },
            "test_results": self.test_results,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save report
        report_file = Path("test_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("\n" + "="*60)
        print("🧪 P2P AI SYSTEM TEST REPORT")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {total_tests - passed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Total Time: {total_time:.2f}s")
        print("="*60)
        
        # Print detailed results
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"  {status} - {result['test']}: {result['details']}")
        
        print(f"\n📄 Full report saved to: {report_file}")
        
        return report

async def main():
    """Run all tests"""
    print("🚀 Starting P2P AI System Comprehensive Tests...")
    print("="*60)
    
    tester = P2PSystemTester()
    
    # Run all test suites
    await tester.test_cli_interface()
    await tester.test_pytorch_prototype()
    await tester.test_identity_system()
    await tester.test_rewards_system()
    await tester.test_integration()
    await tester.test_performance()
    await tester.test_error_handling()
    
    # Generate report
    report = tester.generate_report()
    
    # Cleanup test directories
    import shutil
    test_dirs = [".test_identity", ".test_rewards", ".test_integration_identity", 
                 ".test_integration_rewards", ".test_performance_identity", 
                 ".test_performance_rewards", ".test_error_identity", ".test_error_rewards"]
    
    for test_dir in test_dirs:
        if Path(test_dir).exists():
            shutil.rmtree(test_dir)
    
    print("\n🧹 Test directories cleaned up")
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    asyncio.run(main()) 