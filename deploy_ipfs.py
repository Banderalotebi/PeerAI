#!/usr/bin/env python3
"""
PeerAI IPFS Deployment Workflow
سير عمل نشر PeerAI على IPFS
"""

import asyncio
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

class IPFSDeploymentWorkflow:
    """Complete workflow for deploying PeerAI on IPFS"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.log_file = self.project_dir / "deployment.log"
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        print(log_entry)
        
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")
    
    def check_system_requirements(self) -> bool:
        """Check if system meets requirements"""
        self.log("🔍 Checking system requirements...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or python_version.minor < 8:
            self.log(f"❌ Python 3.8+ required, found {python_version.major}.{python_version.minor}", "ERROR")
            return False
        
        self.log(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check required packages
        required_packages = ['torch', 'pandas', 'numpy']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                self.log(f"✅ {package} installed")
            except ImportError:
                missing_packages.append(package)
                self.log(f"❌ {package} missing", "ERROR")
        
        if missing_packages:
            self.log(f"Install missing packages: pip install {' '.join(missing_packages)}", "ERROR")
            return False
        
        return True
    
    def check_ipfs_installation(self) -> bool:
        """Check IPFS installation and status"""
        self.log("🔍 Checking IPFS installation...")
        
        try:
            # Check if IPFS is installed
            result = subprocess.run(['ipfs', 'version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.log("❌ IPFS not installed", "ERROR")
                return False
            
            version = result.stdout.strip()
            self.log(f"✅ IPFS installed: {version}")
            
            # Check if IPFS is initialized
            ipfs_dir = Path.home() / ".ipfs"
            if not ipfs_dir.exists():
                self.log("🔧 Initializing IPFS...")
                subprocess.run(['ipfs', 'init'], check=True)
                self.log("✅ IPFS initialized")
            
            # Check if daemon is running
            try:
                result = subprocess.run(['ipfs', 'id'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    peer_info = json.loads(result.stdout)
                    self.log(f"✅ IPFS daemon running - Peer ID: {peer_info['ID'][:16]}...")
                    return True
                else:
                    self.log("⚠️  IPFS daemon not running", "WARNING")
                    return False
            except subprocess.TimeoutExpired:
                self.log("⚠️  IPFS daemon not responding", "WARNING")
                return False
                
        except FileNotFoundError:
            self.log("❌ IPFS not found in PATH", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Error checking IPFS: {e}", "ERROR")
            return False
    
    def start_ipfs_daemon(self) -> bool:
        """Start IPFS daemon if not running"""
        self.log("🚀 Starting IPFS daemon...")
        
        try:
            # Start daemon in background
            process = subprocess.Popen(['ipfs', 'daemon'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            # Wait a bit for daemon to start
            import time
            time.sleep(3)
            
            # Check if it's running
            try:
                result = subprocess.run(['ipfs', 'id'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.log("✅ IPFS daemon started successfully")
                    return True
                else:
                    self.log("❌ Failed to start IPFS daemon", "ERROR")
                    return False
            except subprocess.TimeoutExpired:
                self.log("❌ IPFS daemon startup timeout", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error starting IPFS daemon: {e}", "ERROR")
            return False
    
    async def deploy_peerai_models(self) -> bool:
        """Deploy PeerAI models to IPFS"""
        self.log("🤖 Deploying PeerAI models to IPFS...")
        
        try:
            from train_and_share import PeerAIIPFSTrainer
            
            trainer = PeerAIIPFSTrainer()
            
            # Check trainer status
            status = await trainer.get_status()
            if not status['ipfs_connected']:
                self.log("❌ IPFS not connected for deployment", "ERROR")
                return False
            
            self.log(f"📊 Trainer Status:")
            self.log(f"   Node ID: {status['node_id']}")
            self.log(f"   IPFS Peer: {status['ipfs_peer_id'][:16]}...")
            
            # Create and deploy a demo model
            self.log("🎯 Training demo model...")
            model_info = await trainer.create_and_train_model(
                model_type="bert",
                epochs=2,
                description="Demo Arabic sentiment model deployed via workflow"
            )
            
            # Share to IPFS
            upload_result = await trainer.share_model_to_ipfs(model_info)
            
            self.log(f"✅ Model deployed successfully!")
            self.log(f"   CID: {upload_result['cid']}")
            self.log(f"   IPFS URL: {upload_result['ipfs_url']}")
            
            # Save deployment info
            deployment_info = {
                'timestamp': datetime.now().isoformat(),
                'model_cid': upload_result['cid'],
                'model_id': model_info['model_id'],
                'node_id': status['node_id'],
                'ipfs_url': upload_result['ipfs_url']
            }
            
            deployment_file = self.project_dir / "deployment_info.json"
            with open(deployment_file, 'w') as f:
                json.dump(deployment_info, f, indent=2)
            
            self.log(f"📄 Deployment info saved to: {deployment_file}")
            
            return True
            
        except ImportError as e:
            self.log(f"❌ Import error: {e}", "ERROR")
            self.log("Install dependencies: pip install -r requirements_ipfs.txt", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Deployment error: {e}", "ERROR")
            return False
    
    def generate_deployment_report(self, success: bool):
        """Generate deployment report"""
        self.log("📊 Generating deployment report...")
        
        report = {
            'deployment_time': datetime.now().isoformat(),
            'success': success,
            'project_dir': str(self.project_dir),
            'log_file': str(self.log_file)
        }
        
        if success:
            # Check if deployment info exists
            deployment_file = self.project_dir / "deployment_info.json"
            if deployment_file.exists():
                with open(deployment_file, 'r') as f:
                    deployment_info = json.load(f)
                report['deployment_info'] = deployment_info
        
        report_file = self.project_dir / "deployment_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"📄 Deployment report saved to: {report_file}")
        
        # Print summary
        print("\n" + "="*50)
        print("📊 DEPLOYMENT SUMMARY")
        print("="*50)
        
        if success:
            print("✅ PeerAI successfully deployed to IPFS!")
            if 'deployment_info' in report:
                info = report['deployment_info']
                print(f"   Model CID: {info['model_cid']}")
                print(f"   IPFS URL: {info['ipfs_url']}")
                print(f"   Node ID: {info['node_id']}")
            print(f"\n🌐 Your model is now available on the IPFS network!")
            print(f"🔗 Access via: https://ipfs.io/ipfs/{info['model_cid']}")
        else:
            print("❌ Deployment failed. Check the log for details.")
            print(f"📄 Log file: {self.log_file}")
        
        print(f"\n📊 Full report: {report_file}")
    
    async def run_deployment(self):
        """Run the complete deployment workflow"""
        self.log("🌐 Starting PeerAI IPFS Deployment Workflow")
        self.log("="*50)
        
        success = True
        
        # Step 1: Check system requirements
        if not self.check_system_requirements():
            success = False
        
        # Step 2: Check IPFS installation
        if success and not self.check_ipfs_installation():
            # Try to start daemon
            if not self.start_ipfs_daemon():
                success = False
        
        # Step 3: Deploy models (if everything is ready)
        if success:
            if not await self.deploy_peerai_models():
                success = False
        
        # Step 4: Generate report
        self.generate_deployment_report(success)
        
        return success

async def main():
    """Main deployment function"""
    workflow = IPFSDeploymentWorkflow()
    success = await workflow.run_deployment()
    
    if success:
        print("\n🎉 Ready to use PeerAI on IPFS!")
        print("Next steps:")
        print("1. Run: python train_and_share.py")
        print("2. Use CLI: python p2p_ai_cli.py --help")
        print("3. Check docs: IPFS_TRAINING_GUIDE.md")
    else:
        print("\n❌ Deployment failed. Please check the logs and fix any issues.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
