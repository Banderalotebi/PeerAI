#!/usr/bin/env python3
"""
Simple Demo - P2P AI System
عرض توضيحي بسيط - نظام الذكاء الاصطناعي اللامركزي
"""

import asyncio
import sys

def main():
    """Simple demo function"""
    print("🌐 P2P AI Decentralized System")
    print("="*40)
    print("نظام الذكاء الاصطناعي اللامركزي")
    print("="*40)
    
    print("\n🚀 Starting demo...")
    
    try:
        # Test basic imports
        print("1️⃣ Testing imports...")
        
        import click
        print("   ✅ Click imported")
        
        import torch
        print(f"   ✅ PyTorch imported (version: {torch.__version__})")
        
        import transformers
        print(f"   ✅ Transformers imported (version: {transformers.__version__})")
        
        print("\n2️⃣ Testing CLI...")
        import p2p_ai_cli
        print(f"   ✅ CLI loaded - Node ID: {p2p_ai_cli.config.config['node_id']}")
        
        print("\n3️⃣ Testing PyTorch prototype...")
        import p2p_ai_prototype
        prototype = p2p_ai_prototype.P2PAIPrototype("demo_node")
        print(f"   ✅ PyTorch prototype loaded - Device: {prototype.device}")
        
        print("\n4️⃣ Testing identity system...")
        import p2p_identity_system
        identity_manager = p2p_identity_system.P2PIdentityManager(".demo_identity")
        print(f"   ✅ Identity system loaded - Node: {identity_manager.get_node_id()}")
        
        print("\n5️⃣ Testing rewards system...")
        import p2p_rewards_system
        rewards_system = p2p_rewards_system.P2PRewardsSystem(".demo_rewards")
        print("   ✅ Rewards system loaded")
        
        print("\n🎉 All components loaded successfully!")
        print("\n💡 Next steps:")
        print("   - Run: python p2p_ai_cli.py --help")
        print("   - Try: python p2p_ai_cli.py connect --topic arabic_news")
        print("   - Test: python test_p2p_system.py")
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("💡 Install missing dependencies:")
        print("   pip install click torch transformers")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check the documentation for troubleshooting")

if __name__ == "__main__":
    main() 