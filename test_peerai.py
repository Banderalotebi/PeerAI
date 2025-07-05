#!/usr/bin/env python3
"""
PeerAI - IPFS Deployment Test and Demo
اختبار وعرض توضيحي لنشر PeerAI على IPFS
"""

import asyncio
import subprocess
import sys
from pathlib import Path

print("🌐 Hello from PeerAI!")
print("=" * 40)

async def check_ipfs_installation():
    """Check if IPFS is installed and running"""
    try:
        # Check if IPFS is installed
        result = subprocess.run(['ipfs', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ IPFS installed: {result.stdout.strip()}")
            
            # Check if IPFS daemon is running
            try:
                result = subprocess.run(['ipfs', 'id'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print("✅ IPFS daemon is running")
                    return True
                else:
                    print("⚠️  IPFS daemon not running")
                    return False
            except subprocess.TimeoutExpired:
                print("⚠️  IPFS daemon not responding")
                return False
        else:
            print("❌ IPFS not installed")
            return False
    except FileNotFoundError:
        print("❌ IPFS not found in PATH")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'torch',
        'pandas', 
        'numpy',
        'pathlib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} missing")
            missing_packages.append(package)
    
    # Check optional IPFS client
    try:
        import ipfshttpclient
        print("✅ ipfshttpclient installed")
    except ImportError:
        print("⚠️  ipfshttpclient missing (install with: pip install ipfshttpclient)")
        missing_packages.append('ipfshttpclient')
    
    return missing_packages

async def demo_basic_functionality():
    """Demonstrate basic PeerAI functionality"""
    try:
        print("\n🤖 Testing basic AI functionality...")
        
        from p2p_ai_prototype import P2PAIPrototype
        
        # Create AI prototype
        prototype = P2PAIPrototype("demo_node")
        
        # Sample Arabic data
        texts = [
            "هذا منتج رائع",
            "المنتج سيء جداً", 
            "منتج مقبول"
        ]
        labels = [2, 0, 1]  # positive, negative, neutral
        
        # Create and train model
        model_info = await prototype.create_model("bert", num_classes=3)
        model_id = model_info['model_id']
        
        print(f"   Created model: {model_id}")
        
        # Train model
        training_result = await prototype.train_model(
            model_id, texts, labels, epochs=2
        )
        
        print(f"   Training completed - Accuracy: {training_result['final_accuracy']:.2f}%")
        
        # Test prediction
        predictions = await prototype.predict(model_id, ["هذا رائع"])
        sentiment = ["سلبي", "محايد", "إيجابي"][predictions[0]['predicted_class']]
        
        print(f"   Prediction: 'هذا رائع' -> {sentiment}")
        print("✅ Basic AI functionality working!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in basic functionality: {e}")
        return False

async def demo_ipfs_deployment():
    """Demonstrate IPFS deployment"""
    try:
        print("\n📤 Testing IPFS deployment...")
        
        # Check if we can import IPFS integration
        try:
            from train_and_share import PeerAIIPFSTrainer
            print("   IPFS integration module loaded")
        except ImportError as e:
            print(f"   ⚠️  IPFS integration not available: {e}")
            return False
        
        # Create trainer
        trainer = PeerAIIPFSTrainer()
        
        # Get status
        status = await trainer.get_status()
        print(f"   Node ID: {status['node_id']}")
        print(f"   IPFS Connected: {status['ipfs_connected']}")
        
        if status['ipfs_connected']:
            print("   ✅ Ready for IPFS deployment!")
            
            # Run a simple training and sharing demo
            print("   🤖 Creating model for IPFS sharing...")
            
            model_info = await trainer.create_and_train_model(
                epochs=1,  # Quick training for demo
                description="Demo Arabic sentiment model"
            )
            
            print(f"   📤 Uploading to IPFS...")
            upload_result = await trainer.share_model_to_ipfs(model_info)
            
            print(f"   ✅ Model uploaded!")
            print(f"   CID: {upload_result['cid']}")
            print(f"   URL: {upload_result['ipfs_url']}")
            
            return True
        else:
            print("   ⚠️  IPFS not connected - deployment not possible")
            return False
            
    except Exception as e:
        print(f"❌ Error in IPFS deployment: {e}")
        return False

def show_deployment_instructions():
    """Show IPFS deployment instructions"""
    print("\n📚 IPFS Deployment Instructions:")
    print("=" * 40)
    
    print("\n1️⃣ Install IPFS:")
    print("   macOS: brew install ipfs")
    print("   Ubuntu: wget + install from ipfs.io")
    print("   Windows: Download from ipfs.io")
    
    print("\n2️⃣ Initialize and start IPFS:")
    print("   $ ipfs init")
    print("   $ ipfs daemon")
    
    print("\n3️⃣ Install Python dependencies:")
    print("   $ pip install -r requirements_ipfs.txt")
    print("   $ pip install ipfshttpclient")
    
    print("\n4️⃣ Deploy your models:")
    print("   $ python train_and_share.py")
    
    print("\n5️⃣ Use CLI interface:")
    print("   $ python p2p_ai_cli.py --help")
    
    print("\n📖 Full guide: IPFS_TRAINING_GUIDE.md")

async def main():
    """Main demo function"""
    print("Starting PeerAI IPFS deployment test...\n")
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
    
    # Check IPFS
    print(f"\n🔍 Checking IPFS installation...")
    ipfs_ready = await check_ipfs_installation()
    
    # Test basic functionality
    basic_working = await demo_basic_functionality()
    
    # Test IPFS deployment (if IPFS is ready)
    if ipfs_ready and basic_working:
        ipfs_working = await demo_ipfs_deployment()
    else:
        ipfs_working = False
    
    # Show results
    print(f"\n📊 Test Results:")
    print(f"   Basic AI: {'✅ Working' if basic_working else '❌ Failed'}")
    print(f"   IPFS Ready: {'✅ Ready' if ipfs_ready else '❌ Not Ready'}")
    print(f"   IPFS Deploy: {'✅ Working' if ipfs_working else '❌ Not Working'}")
    
    # Show instructions if needed
    if not ipfs_ready or not ipfs_working:
        show_deployment_instructions()
    else:
        print(f"\n🎉 PeerAI is ready for IPFS deployment!")
        print(f"   Run: python train_and_share.py")
        print(f"   Or:  python p2p_ai_cli.py")

if __name__ == "__main__":
    asyncio.run(main())
