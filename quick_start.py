#!/usr/bin/env python3
"""
Quick Start Demo - P2P AI Decentralized System
عرض سريع - نظام الذكاء الاصطناعي اللامركزي
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

def print_banner():
    """Print system banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║  🌐 P2P AI Decentralized System                             ║
    ║  نظام الذكاء الاصطناعي اللامركزي                             ║
    ║                                                              ║
    ║  A revolutionary decentralized AI training and              ║
    ║  knowledge exchange system                                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_menu():
    """Print main menu"""
    menu = """
    🎯 Choose an option / اختر خياراً:
    
    1. 🚀 Quick Demo - Complete Workflow
    2. 🖥️  CLI Interface Demo
    3. 🤖 PyTorch Model Demo
    4. 🔐 Identity & Security Demo
    5. 💰 Rewards System Demo
    6. 🧪 Run All Tests
    7. 📊 System Status
    8. ❌ Exit
    
    Enter your choice (1-8): """
    return input(menu)

async def quick_demo():
    """Complete workflow demonstration"""
    print("\n🚀 Starting Quick Demo - Complete Workflow...")
    print("="*50)
    
    try:
        # Import all components
        import p2p_ai_cli
        import p2p_ai_prototype
        import p2p_identity_system
        import p2p_rewards_system
        
        print("✅ All components loaded successfully")
        
        # Initialize components
        cli_config = p2p_ai_cli.config
        cli_node = p2p_ai_cli.node
        prototype = p2p_ai_prototype.P2PAIPrototype("demo_node")
        identity_manager = p2p_identity_system.P2PIdentityManager(".demo_identity")
        rewards_system = p2p_rewards_system.P2PRewardsSystem(".demo_rewards")
        
        print(f"✅ Node ID: {identity_manager.get_node_id()}")
        
        # Step 1: Connect to topic
        print("\n1️⃣ Connecting to topic...")
        success = await cli_node.connect_to_topic("arabic_ai_demo")
        print(f"   {'✅ Connected' if success else '❌ Failed'}")
        
        # Step 2: Fetch data
        print("\n2️⃣ Fetching data from network...")
        try:
            data = await cli_node.fetch_data(10)
            print(f"   ✅ Fetched {len(data)} data points")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Step 3: Add Arabic training data
        print("\n3️⃣ Adding Arabic training data...")
        arabic_texts = [
            "هذا نص إيجابي جميل",
            "هذا نص سلبي سيء",
            "هذا نص محايد عادي",
            "أحب هذا المنتج كثيراً",
            "لا أحب هذا المنتج إطلاقاً",
            "هذا المنتج مقبول",
            "ممتاز جداً هذا التطبيق",
            "سيء جداً هذا التطبيق",
            "هذا التطبيق عادي"
        ]
        labels = [2, 0, 1, 2, 0, 1, 2, 0, 1]  # 0=negative, 1=neutral, 2=positive
        
        data_count = await prototype.add_data(arabic_texts, labels)
        print(f"   ✅ Added {data_count} Arabic text samples")
        
        # Step 4: Create and train model
        print("\n4️⃣ Creating and training BERT model...")
        model_info = await prototype.create_model("bert", num_classes=3)
        model_id = model_info['model_id']
        print(f"   ✅ Created model: {model_id}")
        
        training_result = await prototype.train_model(model_id, arabic_texts, labels, epochs=3)
        print(f"   ✅ Training completed - Accuracy: {training_result['final_accuracy']:.2f}%")
        
        # Step 5: Make predictions
        print("\n5️⃣ Making predictions on new Arabic text...")
        test_texts = ["أحب هذا كثيراً", "لا أحب هذا", "هذا مقبول", "ممتاز جداً"]
        predictions = await prototype.predict(model_id, test_texts)
        
        print("   📊 Predictions:")
        for pred in predictions:
            sentiment = ["سلبي", "محايد", "إيجابي"][pred['predicted_class']]
            confidence = pred['confidence']
            print(f"      '{pred['text']}' -> {sentiment} (confidence: {confidence:.2f})")
        
        # Step 6: Extract knowledge
        print("\n6️⃣ Extracting knowledge from trained model...")
        knowledge = await cli_node.extract_knowledge("sentiment")
        print(f"   ✅ Knowledge extracted - Confidence: {knowledge['confidence']:.2f}")
        print("   📋 Insights:")
        for i, insight in enumerate(knowledge['insights'], 1):
            print(f"      {i}. {insight}")
        
        # Step 7: Create signature and publish contribution
        print("\n7️⃣ Creating signature and publishing contribution...")
        contribution_data = f"trained_model_{model_id}_accuracy_{training_result['final_accuracy']:.2f}"
        signature = identity_manager.create_signature(contribution_data)
        print(f"   ✅ Signature created: {signature.signature[:20]}...")
        
        # Step 8: Record contribution and earn rewards
        print("\n8️⃣ Recording contribution and earning rewards...")
        reward_result = rewards_system.record_contribution(
            node_id=identity_manager.get_node_id(),
            contribution_type="model_training",
            data_hash=contribution_data,
            quality_score=training_result['final_accuracy'] / 100.0,
            signature=signature.signature
        )
        
        print(f"   ✅ Earned {reward_result['reward_amount']} tokens")
        print(f"   💰 New balance: {reward_result['new_balance']} tokens")
        
        # Step 9: Show results
        print("\n9️⃣ Final Results:")
        balance = rewards_system.get_balance(identity_manager.get_node_id())
        reputation = rewards_system.get_reputation(identity_manager.get_node_id())
        
        print(f"   💰 Total tokens: {balance}")
        print(f"   🏆 Reputation tier: {reputation['tier']}")
        print(f"   🤝 Trust level: {reputation['trust_level']:.2f}")
        
        # Step 10: Show leaderboard
        print("\n🔟 Current Leaderboard:")
        leaderboard = rewards_system.get_leaderboard(3)
        for entry in leaderboard:
            print(f"   {entry['rank']}. {entry['node_id']} - {entry['total_tokens']} tokens ({entry['tier']})")
        
        print("\n🎉 Quick Demo completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

async def cli_demo():
    """CLI interface demonstration"""
    print("\n🖥️ CLI Interface Demo...")
    print("="*30)
    
    try:
        import p2p_ai_cli
        
        # Show status
        print("📊 Current Node Status:")
        cli_node = p2p_ai_cli.node
        print(f"   Node ID: {cli_node.config.config['node_id']}")
        print(f"   Connected: {cli_node.connected}")
        print(f"   Current Topic: {cli_node.current_topic or 'None'}")
        
        # Show available commands
        print("\n📋 Available Commands:")
        commands = [
            "connect --topic arabic_news",
            "fetch-data --limit 50",
            "train --algorithm bert --epochs 3",
            "extract --task sentiment",
            "publish --type model_training",
            "leaderboard",
            "status"
        ]
        
        for i, cmd in enumerate(commands, 1):
            print(f"   {i}. python p2p_ai_cli.py {cmd}")
        
        print("\n💡 Try running these commands to explore the system!")
        
    except Exception as e:
        print(f"❌ CLI demo error: {e}")

async def pytorch_demo():
    """PyTorch model demonstration"""
    print("\n🤖 PyTorch Model Demo...")
    print("="*30)
    
    try:
        import p2p_ai_prototype
        
        # Create prototype
        prototype = p2p_ai_prototype.P2PAIPrototype("pytorch_demo_node")
        print(f"✅ Created prototype on device: {prototype.device}")
        
        # Sample data
        texts = ["نص تجريبي", "Test text", "مثال آخر", "Another example"]
        labels = [0, 1, 2, 1]
        
        # Add data
        data_count = await prototype.add_data(texts, labels)
        print(f"✅ Added {data_count} data points")
        
        # Create model
        model_info = await prototype.create_model("bert", num_classes=3)
        model_id = model_info['model_id']
        print(f"✅ Created model: {model_id}")
        
        # Train model
        print("🔄 Training model...")
        training_result = await prototype.train_model(model_id, texts, labels, epochs=2)
        print(f"✅ Training completed - Accuracy: {training_result['final_accuracy']:.2f}%")
        
        # Make predictions
        test_texts = ["نص للاختبار", "Test prediction"]
        predictions = await prototype.predict(model_id, test_texts)
        
        print("📊 Predictions:")
        for pred in predictions:
            sentiment = ["سلبي", "محايد", "إيجابي"][pred['predicted_class']]
            print(f"   '{pred['text']}' -> {sentiment} (confidence: {pred['confidence']:.2f})")
        
        # Save model
        await prototype.save_model(model_id)
        print(f"✅ Model saved successfully")
        
    except Exception as e:
        print(f"❌ PyTorch demo error: {e}")

async def identity_demo():
    """Identity and security demonstration"""
    print("\n🔐 Identity & Security Demo...")
    print("="*35)
    
    try:
        import p2p_identity_system
        
        # Create identity manager
        identity_manager = p2p_identity_system.P2PIdentityManager(".identity_demo")
        print(f"✅ Created identity manager for node: {identity_manager.get_node_id()}")
        
        # Test signature creation and verification
        test_data = "Hello, P2P AI Network! مرحباً بشبكة الذكاء الاصطناعي اللامركزية!"
        
        print(f"\n📝 Creating signature for: {test_data}")
        signature = identity_manager.create_signature(test_data)
        print(f"✅ Signature created: {signature.signature[:30]}...")
        print(f"   Algorithm: {signature.algorithm}")
        
        # Verify signature
        is_valid = identity_manager.verify_signature(test_data, signature)
        print(f"✅ Signature verification: {'PASS' if is_valid else 'FAIL'}")
        
        # Test invalid signature
        is_invalid = identity_manager.verify_signature("Invalid data", signature)
        print(f"✅ Invalid data test: {'PASS' if not is_invalid else 'FAIL'}")
        
        # Add another identity
        other_node_id = "demo_node_456"
        other_public_key = "demo_public_key_123"
        success = identity_manager.add_identity(other_node_id, other_public_key)
        print(f"\n✅ Added identity: {other_node_id}")
        
        # Update reputation
        identity_manager.update_reputation(other_node_id, 15.0)
        print(f"✅ Updated reputation for {other_node_id}")
        
        # Get trusted nodes
        trusted_nodes = identity_manager.get_trusted_nodes()
        print(f"✅ Found {len(trusted_nodes)} trusted nodes")
        
        # Export identity
        exported_identity = identity_manager.export_identity()
        print(f"\n📤 Exported identity: {exported_identity['node_id']}")
        
    except Exception as e:
        print(f"❌ Identity demo error: {e}")

async def rewards_demo():
    """Rewards system demonstration"""
    print("\n💰 Rewards System Demo...")
    print("="*30)
    
    try:
        import p2p_rewards_system
        
        # Create rewards system
        rewards_system = p2p_rewards_system.P2PRewardsSystem(".rewards_demo")
        print("✅ Created rewards system")
        
        # Test different contribution types
        contribution_types = [
            ("data_contribution", 0.7),
            ("model_training", 0.85),
            ("knowledge_extraction", 0.9),
            ("validation", 0.75)
        ]
        
        print("\n📊 Recording contributions...")
        for contrib_type, quality in contribution_types:
            result = rewards_system.record_contribution(
                node_id=f"demo_node_{contrib_type}",
                contribution_type=contrib_type,
                data_hash=f"hash_{contrib_type}",
                quality_score=quality
            )
            print(f"   {contrib_type}: {result['reward_amount']} tokens (quality: {quality})")
        
        # Show leaderboard
        print("\n🏆 Current Leaderboard:")
        leaderboard = rewards_system.get_leaderboard(5)
        for entry in leaderboard:
            print(f"   {entry['rank']}. {entry['node_id']} - {entry['total_tokens']} tokens ({entry['tier']})")
        
        # Show network stats
        print("\n📈 Network Statistics:")
        stats = rewards_system.get_network_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Test token transfer
        print("\n💸 Testing token transfer...")
        success = rewards_system.transfer_tokens("demo_node_model_training", "demo_node_data_contribution", 5.0)
        print(f"   Transfer result: {'SUCCESS' if success else 'FAILED'}")
        
        # Show updated balances
        print("\n💰 Updated Balances:")
        for contrib_type, _ in contribution_types:
            node_id = f"demo_node_{contrib_type}"
            balance = rewards_system.get_balance(node_id)
            reputation = rewards_system.get_reputation(node_id)
            print(f"   {node_id}: {balance} tokens, Tier: {reputation['tier']}")
        
    except Exception as e:
        print(f"❌ Rewards demo error: {e}")

async def run_tests():
    """Run comprehensive tests"""
    print("\n🧪 Running Comprehensive Tests...")
    print("="*35)
    
    try:
        import test_p2p_system
        await test_p2p_system.main()
    except Exception as e:
        print(f"❌ Test error: {e}")

async def system_status():
    """Show system status"""
    print("\n📊 System Status...")
    print("="*20)
    
    try:
        # Check if components are available
        components = {
            "CLI Interface": "p2p_ai_cli.py",
            "PyTorch Prototype": "p2p_ai_prototype.py",
            "Identity System": "p2p_identity_system.py",
            "Rewards System": "p2p_rewards_system.py",
            "Test Suite": "test_p2p_system.py"
        }
        
        print("🔍 Checking component availability:")
        for name, file in components.items():
            if Path(file).exists():
                print(f"   ✅ {name}: Available")
            else:
                print(f"   ❌ {name}: Missing")
        
        # Check configuration directories
        config_dirs = [
            "~/.p2p_ai",
            ".p2p_identity",
            ".p2p_rewards"
        ]
        
        print("\n📁 Configuration directories:")
        for config_dir in config_dirs:
            dir_path = Path(config_dir).expanduser()
            if dir_path.exists():
                print(f"   ✅ {config_dir}: Exists")
            else:
                print(f"   ❌ {config_dir}: Missing")
        
        # Show system info
        print(f"\n💻 System Information:")
        print(f"   Python version: {asyncio.get_event_loop().get_debug()}")
        print(f"   Current directory: {Path.cwd()}")
        print(f"   Timestamp: {datetime.now().isoformat()}")
        
    except Exception as e:
        print(f"❌ Status check error: {e}")

async def main():
    """Main demo function"""
    print_banner()
    
    while True:
        choice = print_menu()
        
        if choice == "1":
            await quick_demo()
        elif choice == "2":
            await cli_demo()
        elif choice == "3":
            await pytorch_demo()
        elif choice == "4":
            await identity_demo()
        elif choice == "5":
            await rewards_demo()
        elif choice == "6":
            await run_tests()
        elif choice == "7":
            await system_status()
        elif choice == "8":
            print("\n👋 Thank you for exploring the P2P AI System!")
            print("شكراً لك لاستكشاف نظام الذكاء الاصطناعي اللامركزي!")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number between 1-8.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    asyncio.run(main()) 