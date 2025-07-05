#!/usr/bin/env python3
"""
PeerAI IPFS CLI Tool
أداة سطر الأوامر لإدارة PeerAI على IPFS
"""

import click
import asyncio
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Import your existing IPFS integration
try:
    from ipfs_integration import PeerAIIPFS
    from deploy_ipfs import IPFSDeploymentWorkflow
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the correct directory and dependencies are installed")
    sys.exit(1)

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """PeerAI IPFS Management CLI"""
    pass

@cli.group()
def deploy():
    """Deployment commands"""
    pass

@deploy.command()
@click.option('--type', 'deployment_type', 
              type=click.Choice(['local', 'docker', 'cloud']), 
              default='local', help='Deployment type')
@click.option('--node-id', default=None, help='Custom node ID')
def start(deployment_type: str, node_id: str):
    """Start PeerAI IPFS deployment"""
    click.echo(f"🚀 Starting {deployment_type} deployment...")
    
    if deployment_type == 'docker':
        # Use the deployment script
        cmd = ['./deploy.sh', 'docker']
        if node_id:
            cmd.append(node_id)
        subprocess.run(cmd, check=True)
    elif deployment_type == 'local':
        cmd = ['./deploy.sh', 'local']
        if node_id:
            cmd.append(node_id)
        subprocess.run(cmd, check=True)
    else:
        click.echo("☁️  Cloud deployment requires manual setup")
        click.echo("Run: ./deploy.sh cloud")

@deploy.command()
def stop():
    """Stop all services"""
    click.echo("🛑 Stopping services...")
    subprocess.run(['./deploy.sh', 'stop'], check=True)

@deploy.command()
def status():
    """Show deployment status"""
    subprocess.run(['./deploy.sh', 'status'], check=True)

@deploy.command()
def health():
    """Check system health"""
    subprocess.run(['./deploy.sh', 'health'], check=True)

@cli.group()
def ipfs():
    """IPFS management commands"""
    pass

@ipfs.command()
def init():
    """Initialize IPFS node"""
    click.echo("🔧 Initializing IPFS...")
    try:
        subprocess.run(['ipfs', 'init'], check=True)
        click.echo("✅ IPFS initialized successfully")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to initialize IPFS: {e}")

@ipfs.command()
def start_daemon():
    """Start IPFS daemon"""
    click.echo("🚀 Starting IPFS daemon...")
    try:
        subprocess.Popen(['ipfs', 'daemon', '--enable-pubsub-experiment'])
        click.echo("✅ IPFS daemon started")
    except Exception as e:
        click.echo(f"❌ Failed to start IPFS daemon: {e}")

@ipfs.command()
def info():
    """Show IPFS node information"""
    try:
        result = subprocess.run(['ipfs', 'id'], capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)
        click.echo("📊 IPFS Node Information:")
        click.echo(f"   Peer ID: {info['ID']}")
        click.echo(f"   Addresses: {info['Addresses']}")
        click.echo(f"   Agent Version: {info['AgentVersion']}")
        click.echo(f"   Protocol Version: {info['ProtocolVersion']}")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to get IPFS info: {e}")

@ipfs.command()
@click.argument('file_path', type=click.Path(exists=True))
def add(file_path: str):
    """Add file to IPFS"""
    click.echo(f"📤 Adding {file_path} to IPFS...")
    try:
        result = subprocess.run(['ipfs', 'add', file_path], 
                              capture_output=True, text=True, check=True)
        cid = result.stdout.strip().split()[-2]
        click.echo(f"✅ File added with CID: {cid}")
        click.echo(f"🌐 Access via: https://ipfs.io/ipfs/{cid}")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to add file: {e}")

@ipfs.command()
@click.argument('cid')
def get(cid: str):
    """Download file from IPFS"""
    click.echo(f"📥 Downloading {cid} from IPFS...")
    try:
        subprocess.run(['ipfs', 'get', cid], check=True)
        click.echo(f"✅ File downloaded successfully")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to download file: {e}")

@cli.group()
def model():
    """Model management commands"""
    pass

@model.command()
@click.option('--model-type', default='bert', help='Model type')
@click.option('--epochs', default=5, help='Training epochs')
@click.option('--description', help='Model description')
async def train(model_type: str, epochs: int, description: str):
    """Train and deploy a model to IPFS"""
    click.echo("🤖 Training and deploying model...")
    
    try:
        from train_and_share import PeerAIIPFSTrainer
        
        trainer = PeerAIIPFSTrainer()
        
        # Train model
        model_info = await trainer.create_and_train_model(
            model_type=model_type,
            epochs=epochs,
            description=description or f"{model_type} model trained via CLI"
        )
        
        # Share to IPFS
        upload_result = await trainer.share_model_to_ipfs(model_info)
        
        click.echo("✅ Model trained and deployed successfully!")
        click.echo(f"   Model ID: {model_info['model_id']}")
        click.echo(f"   CID: {upload_result['cid']}")
        click.echo(f"   IPFS URL: {upload_result['ipfs_url']}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@model.command()
async def list_models():
    """List available models"""
    click.echo("📋 Available models:")
    
    try:
        ipfs_client = PeerAIIPFS()
        models = await ipfs_client.list_models()
        
        if not models:
            click.echo("   No models found")
            return
        
        for model in models:
            click.echo(f"   📦 {model['model_id']}")
            click.echo(f"      Type: {model['model_type']}")
            click.echo(f"      CID: {model['cid']}")
            click.echo(f"      Created: {model['created_at']}")
            if model.get('accuracy'):
                click.echo(f"      Accuracy: {model['accuracy']:.2f}")
            click.echo()
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@model.command()
@click.argument('cid')
async def download(cid: str):
    """Download model from IPFS"""
    click.echo(f"📥 Downloading model {cid}...")
    
    try:
        ipfs_client = PeerAIIPFS()
        result = await ipfs_client.download_model(cid)
        
        click.echo("✅ Model downloaded successfully!")
        click.echo(f"   Path: {result['download_path']}")
        click.echo(f"   Metadata: {result['metadata']}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@cli.group()
def data():
    """Data management commands"""
    pass

@data.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--data-type', default='csv', help='Data type')
@click.option('--description', help='Data description')
async def upload(file_path: str, data_type: str, description: str):
    """Upload data to IPFS"""
    click.echo(f"📤 Uploading {file_path} to IPFS...")
    
    try:
        ipfs_client = PeerAIIPFS()
        
        data_info = {
            'data_type': data_type,
            'description': description or f"{data_type} data uploaded via CLI",
            'created_at': datetime.now().isoformat()
        }
        
        result = await ipfs_client.upload_data(
            Path(file_path), 
            data_info, 
            node_id="cli-node"
        )
        
        click.echo("✅ Data uploaded successfully!")
        click.echo(f"   CID: {result['cid']}")
        click.echo(f"   IPFS URL: {result['ipfs_url']}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@data.command()
async def list_datasets():
    """List available datasets"""
    click.echo("📋 Available datasets:")
    
    try:
        ipfs_client = PeerAIIPFS()
        datasets = await ipfs_client.list_data()
        
        if not datasets:
            click.echo("   No datasets found")
            return
        
        for dataset in datasets:
            click.echo(f"   📊 {dataset['data_id']}")
            click.echo(f"      Type: {dataset['data_type']}")
            click.echo(f"      CID: {dataset['cid']}")
            click.echo(f"      Size: {dataset['file_size']} bytes")
            click.echo(f"      Created: {dataset['created_at']}")
            click.echo()
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")

@cli.command()
def version():
    """Show version information"""
    click.echo("PeerAI IPFS CLI v1.0.0")
    click.echo("Built with ❤️ for decentralized AI")

@cli.command()
def check():
    """Check system requirements"""
    click.echo("🔍 Checking system requirements...")
    
    # Check IPFS
    try:
        result = subprocess.run(['ipfs', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            click.echo(f"✅ IPFS: {result.stdout.strip()}")
        else:
            click.echo("❌ IPFS not installed")
    except FileNotFoundError:
        click.echo("❌ IPFS not found in PATH")
    
    # Check Python packages
    required_packages = ['torch', 'pandas', 'numpy', 'ipfshttpclient']
    for package in required_packages:
        try:
            __import__(package)
            click.echo(f"✅ {package}")
        except ImportError:
            click.echo(f"❌ {package} not installed")

def main():
    """Main entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 