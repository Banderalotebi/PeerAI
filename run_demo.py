#!/usr/bin/env python3
"""
Simple Demo Runner - P2P AI System
تشغيل العرض التوضيحي البسيط - نظام الذكاء الاصطناعي اللامركزي
"""

import asyncio
import sys
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are available"""
    missing = []
    
    try:
        import click
    except ImportError:
        missing.append("click")
    
    try:
        import torch
    except ImportError:
        missing.append("torch")
    
    try:
        import transformers
    except ImportError:
        missing.append("transformers")
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("💡 Install with: pip install " + " ".join(missing))
        return False
    
    return True

async def run_basic_demo():
    """Run a basic demonstration"""
    print("🚀 Starting Basic P2P AI Demo...")
    print("="*40)
    
    try:
        # Test CLI
        print("1️⃣ Testing CLI Interface...")
        import p2p_ai_cli
        print(f"   ✅ CLI loaded - Node ID: {p2p_ai_cli.config.config['node_id']}")
        
        # Test PyTorch
        print("\n2️⃣ Testing PyTorch Prototype...")
        import p2p_ai_prototype
        prototype = p2p_ai_prototype.P2PAIPrototype("demo_node")
        print(f"   ✅ PyTorch loaded - Device: {prototype.device}")
        
        # Test Identity
        print("\n3️⃣ Testing Identity System...")
        import p2p_identity_system
        identity_manager = p2p_identity_system.P2PIdentityManager(".demo_identity")
        print(f"   ✅ Identity system loaded - Node: {identity_manager.get_node_id()}")
        
        # Test Rewards
        print("\n4️⃣ Testing Rewards System...")
        import p2p_rewards_system
        rewards_system = p2p_rewards_system.P2PRewardsSystem(".demo_rewards")
        print("   ✅ Rewards system loaded")
        
        # Simple workflow
        print("\n5️⃣ Running Simple Workflow...")
        
        # Add data
        texts = ["نص إيجابي", "نص سلبي", "نص محايد"]
        labels = [2, 0, 1]
        await prototype.add_data(texts, labels)
        print("   ✅ Added Arabic training data")
        
        # Create model
        model_info = await prototype.create_model("bert", num_classes=3)
        model_id = model_info['model_id']
        print(f"   ✅ Created model: {model_id}")
        
        # Train model
        result = await prototype.train_model(model_id, texts, labels, epochs=1)
        print(f"   ✅ Trained model - Accuracy: {result['final_accuracy']:.2f}%")
        
        # Make prediction
        predictions = await prototype.predict(model_id, ["أحب هذا"])
        sentiment = ["سلبي", "محايد", "إيجابي"][predictions[0]['predicted_class']]
        print(f"   ✅ Prediction: 'أحب هذا' -> {sentiment}")
        
        # Record contribution
        reward_result = rewards_system.record_contribution(
            node_id=identity_manager.get_node_id(),
            contribution_type="model_training",
            data_hash=f"model_{model_id}",
            quality_score=0.8
        )
        print(f"   ✅ Earned {reward_result['reward_amount']} tokens")
        
        print("\n🎉 Basic demo completed successfully!")
        print("💡 Run 'python quick_start.py' for interactive demo")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("💡 Check dependencies and try again")

def main():
    """Main function"""
    print("🌐 P2P AI Decentralized System - Basic Demo")
    print("="*50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Run demo
    asyncio.run(run_basic_demo())

if __name__ == "__main__":
    main() 