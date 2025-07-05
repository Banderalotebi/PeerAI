#!/bin/bash
# PeerAI IPFS Setup Script
# سكريبت إعداد PeerAI IPFS

echo "🌐 PeerAI IPFS Setup Script"
echo "========================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed"
    exit 1
fi

echo "✅ pip3 found"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."

# Core dependencies
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install pandas numpy scikit-learn
pip3 install click pathlib dataclasses

# IPFS client
pip3 install ipfshttpclient

echo "✅ Python dependencies installed"

# Check if IPFS is installed
echo ""
echo "🔍 Checking IPFS installation..."

if command -v ipfs &> /dev/null; then
    echo "✅ IPFS found: $(ipfs version)"
    
    # Check if IPFS is initialized
    if [ -d ~/.ipfs ]; then
        echo "✅ IPFS already initialized"
    else
        echo "🔧 Initializing IPFS..."
        ipfs init
        echo "✅ IPFS initialized"
    fi
    
    # Check if IPFS daemon is running
    if ipfs id &> /dev/null; then
        echo "✅ IPFS daemon is running"
    else
        echo "⚠️  IPFS daemon not running"
        echo "Start with: ipfs daemon"
    fi
else
    echo "❌ IPFS not found. Installing..."
    
    # Detect OS and install IPFS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "🍺 Installing IPFS via Homebrew..."
            brew install ipfs
        else
            echo "❌ Homebrew not found. Please install IPFS manually from https://ipfs.io/"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "🐧 Installing IPFS for Linux..."
        wget https://dist.ipfs.io/go-ipfs/v0.14.0/go-ipfs_v0.14.0_linux-amd64.tar.gz
        tar -xzf go-ipfs_v0.14.0_linux-amd64.tar.gz
        cd go-ipfs
        sudo ./install.sh
        cd ..
        rm -rf go-ipfs go-ipfs_v0.14.0_linux-amd64.tar.gz
        
        # Initialize IPFS
        ipfs init
    else
        echo "❌ Unsupported OS. Please install IPFS manually from https://ipfs.io/"
        exit 1
    fi
fi

echo ""
echo "🎯 Setup Summary:"
echo "=================="
echo "✅ Python dependencies installed"
echo "✅ IPFS installed"
echo ""
echo "🚀 Next Steps:"
echo "1. Start IPFS daemon: ipfs daemon"
echo "2. Test the system: python3 test_peerai.py"
echo "3. Run training demo: python3 train_and_share.py"
echo "4. Use CLI: python3 p2p_ai_cli.py --help"
echo ""
echo "📚 Documentation: IPFS_TRAINING_GUIDE.md"
echo ""
echo "🎉 PeerAI IPFS setup completed!"
