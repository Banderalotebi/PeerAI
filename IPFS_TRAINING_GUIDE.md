# 🌐 PeerAI - IPFS Deployment Guide
## دليل نشر PeerAI على IPFS

Complete guide for deploying your PeerAI system on the InterPlanetary File System (IPFS) for decentralized model sharing and training.

دليل شامل لنشر نظام PeerAI على نظام الملفات بين الكواكب (IPFS) للمشاركة اللامركزية والتدريب.

---

## 🚀 Quick Start

### 1. Install IPFS

#### Option A: Official IPFS Desktop
```bash
# Download from: https://ipfs.io/
# Install IPFS Desktop for GUI interface
```

#### Option B: Command Line Installation
```bash
# macOS
brew install ipfs

# Ubuntu/Debian
wget https://dist.ipfs.io/go-ipfs/v0.14.0/go-ipfs_v0.14.0_linux-amd64.tar.gz
tar -xzf go-ipfs_v0.14.0_linux-amd64.tar.gz
cd go-ipfs
sudo ./install.sh

# Windows
# Download from: https://dist.ipfs.io/go-ipfs/latest/go-ipfs_latest_windows-amd64.zip
```

### 2. Initialize IPFS Node
```bash
# Initialize IPFS repository
ipfs init

# Start IPFS daemon
ipfs daemon
```

### 3. Install PeerAI IPFS Dependencies
```bash
# Install IPFS Python client
pip install -r requirements_ipfs.txt

# Additional dependencies
pip install ipfshttpclient>=0.8.0
```

---

## 📦 System Architecture

```
PeerAI IPFS Integration
├── 🔗 IPFS Network
│   ├── Model Storage (CID-based)
│   ├── Training Data Storage
│   └── Metadata Registry
├── 🤖 Local AI Engine
│   ├── PyTorch Models
│   ├── Training Pipeline
│   └── Prediction System
└── 🔐 P2P Security
    ├── Node Identity
    ├── Content Verification
    └── Reputation System
```

---

## 🛠 Implementation Steps

### Step 1: Setup IPFS Integration

Create your IPFS-enabled PeerAI node:

```python
from ipfs_integration import PeerAIIPFS
from p2p_ai_prototype import P2PAIPrototype

# Initialize IPFS integration
ipfs_ai = PeerAIIPFS(ipfs_host='localhost', ipfs_port=5001)

# Initialize AI prototype
prototype = P2PAIPrototype("your_node_id")
```

### Step 2: Upload Models to IPFS

```python
# Train a model locally
texts = ["نص تجريبي", "another test"]
labels = [1, 0]

model_info = await prototype.create_model("bert")
await prototype.train_model(model_info['model_id'], texts, labels)

# Upload to IPFS
model_path = Path(f"models/{model_info['model_id']}.pth")
upload_result = await ipfs_ai.upload_model(
    model_path=model_path,
    model_info=model_info,
    node_id="your_node_id"
)

print(f"Model CID: {upload_result['cid']}")
print(f"IPFS URL: {upload_result['ipfs_url']}")
```

### Step 3: Share Training Data

```python
# Upload training data
import pandas as pd

# Create sample data
data = pd.DataFrame({
    'text': ['مثال إيجابي', 'مثال سلبي'],
    'label': [1, 0]
})
data_path = Path("data/sample_data.csv")
data.to_csv(data_path, index=False)

data_info = {
    'data_id': 'arabic_sentiment_001',
    'data_type': 'sentiment_analysis',
    'sample_count': len(data),
    'features': ['text', 'label'],
    'description': 'Arabic sentiment analysis dataset'
}

upload_result = await ipfs_ai.upload_data(
    data_path=data_path,
    data_info=data_info,
    node_id="your_node_id"
)
```

### Step 4: Download and Use Shared Models

```python
# Search for models
models = await ipfs_ai.search_models("sentiment")

# Download a specific model
cid = "QmYourModelCID"
download_result = await ipfs_ai.download_model(cid)

# Load the model
model_path = Path(download_result['download_path']) / "model.pth"
await prototype.load_model("downloaded_model")
```

---

## 🎯 Advanced Features

### Model Versioning
```python
# Create versioned model uploads
model_info = {
    'model_id': 'arabic_bert_v2',
    'version': '2.0.0',
    'parent_cid': 'QmPreviousVersionCID',
    'changelog': 'Improved accuracy by 5%'
}
```

### Content Pinning
```python
# Pin important models to keep them available
await ipfs_ai.pin_content("QmImportantModelCID")

# Unpin when no longer needed
await ipfs_ai.unpin_content("QmOldModelCID")
```

### Metadata Management
```python
# List all available models
models = await ipfs_ai.list_models()
for model in models:
    print(f"Model: {model['model_id']} - CID: {model['cid']}")

# Check IPFS status
status = ipfs_ai.get_ipfs_status()
print(f"Connected: {status['connected']}")
print(f"Peer ID: {status['peer_id']}")
```

---

## 🔧 Configuration

### IPFS Node Configuration
```bash
# Configure IPFS for better performance
ipfs config Addresses.API /ip4/0.0.0.0/tcp/5001
ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/8080

# Enable experimental features
ipfs config --json Experimental.FilestoreEnabled true
ipfs config --json Experimental.UrlstoreEnabled true
```

### PeerAI IPFS Settings
```python
# Custom IPFS configuration
ipfs_ai = PeerAIIPFS(
    ipfs_host='localhost',
    ipfs_port=5001,
    storage_dir='.peerai_ipfs',
    auto_pin=True,
    compression=True
)
```

---

## 🌟 Benefits of IPFS Deployment

### ✅ **Decentralization**
- No single point of failure
- Distributed content storage
- Global accessibility

### ✅ **Immutability**
- Content-addressed storage
- Cryptographic verification
- Version tracking

### ✅ **Efficiency**
- Deduplication
- Caching and CDN-like performance
- Bandwidth optimization

### ✅ **Resilience**
- Automatic replication
- Fault tolerance
- Network healing

---

## 🚨 Troubleshooting

### Common Issues

#### IPFS Connection Failed
```bash
# Check if IPFS daemon is running
ipfs id

# Restart IPFS daemon
ipfs daemon --enable-gc
```

#### Upload Errors
```python
# Check IPFS status
status = ipfs_ai.get_ipfs_status()
if not status['connected']:
    print("IPFS not connected. Start daemon first.")
```

#### Large File Uploads
```bash
# Increase IPFS file size limits
ipfs config Datastore.StorageMax 50GB
```

---

## 📊 Monitoring and Analytics

### Track Model Usage
```python
# Get model download statistics
model_stats = await ipfs_ai.get_model_stats("QmModelCID")
print(f"Downloads: {model_stats['download_count']}")
print(f"Peers: {model_stats['peer_count']}")
```

### Network Health
```bash
# Check IPFS network connectivity
ipfs swarm peers | wc -l

# Monitor bandwidth usage
ipfs stats bw
```

---

## 🔮 Next Steps

1. **Deploy your first model** to IPFS
2. **Join the PeerAI network** by connecting to other nodes
3. **Contribute training data** and earn rewards
4. **Collaborate** on model improvements
5. **Scale** your deployment across multiple nodes

---

## 📚 Resources

- [IPFS Documentation](https://docs.ipfs.io/)
- [PeerAI GitHub Repository](https://github.com/your-repo)
- [Python IPFS Client](https://pypi.org/project/ipfshttpclient/)
- [IPFS Best Practices](https://docs.ipfs.io/how-to/)

---

**Ready to deploy?** Start with the Quick Start section above! 🚀
