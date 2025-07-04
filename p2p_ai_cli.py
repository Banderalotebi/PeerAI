#!/usr/bin/env python3
"""
P2P AI Decentralized System - CLI Interface
نظام الذكاء الاصطناعي اللامركزي - واجهة سطر الأوامر
"""

import click
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class P2PAIConfig:
    """Configuration manager for P2P AI system"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".p2p_ai"
        self.config_file = self.config_dir / "config.json"
        self.ledger_file = self.config_dir / "ledger.json"
        self.models_dir = self.config_dir / "models"
        self.data_dir = self.config_dir / "data"
        
        # Create directories if they don't exist
        self.config_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize config
        self.load_config()
    
    def load_config(self):
        """Load or create configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "node_id": self.generate_node_id(),
                "peers": [],
                "topics": [],
                "current_topic": None,
                "model_settings": {
                    "default_algorithm": "bert",
                    "default_epochs": 3,
                    "batch_size": 32
                },
                "rewards": {
                    "data_contribution": 5,
                    "model_training": 10,
                    "knowledge_extraction": 15
                }
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def generate_node_id(self):
        """Generate unique node ID"""
        import uuid
        return f"node_{uuid.uuid4().hex[:8]}"
    
    def load_ledger(self):
        """Load rewards ledger"""
        if self.ledger_file.exists():
            with open(self.ledger_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_ledger(self, ledger):
        """Save rewards ledger"""
        with open(self.ledger_file, 'w', encoding='utf-8') as f:
            json.dump(ledger, f, indent=2, ensure_ascii=False)

class P2PAINode:
    """P2P AI Node implementation"""
    
    def __init__(self, config):
        self.config = config
        self.connected = False
        self.current_topic = None
        self.local_data = []
        self.local_models = {}
    
    async def connect_to_topic(self, topic):
        """Connect to a specific topic/network"""
        try:
            # Simulate connection
            await asyncio.sleep(1)
            self.current_topic = topic
            self.connected = True
            
            if topic not in self.config.config["topics"]:
                self.config.config["topics"].append(topic)
                self.config.save_config()
            
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    async def fetch_data(self, limit=100):
        """Fetch data from the network"""
        if not self.connected:
            raise Exception("Not connected to any topic")
        
        # Simulate data fetching
        await asyncio.sleep(2)
        
        # Generate mock data
        mock_data = []
        for i in range(min(limit, 50)):
            mock_data.append({
                "id": f"data_{i}",
                "content": f"Sample Arabic text {i} - نص عربي تجريبي {i}",
                "timestamp": datetime.now().isoformat(),
                "source": "network"
            })
        
        self.local_data.extend(mock_data)
        return mock_data
    
    async def train_model(self, algorithm="bert", epochs=3):
        """Train a local model"""
        if not self.local_data:
            raise Exception("No data available for training")
        
        # Simulate training
        await asyncio.sleep(epochs * 2)
        
        model_info = {
            "algorithm": algorithm,
            "epochs": epochs,
            "data_size": len(self.local_data),
            "trained_at": datetime.now().isoformat(),
            "accuracy": 0.85 + (epochs * 0.02),  # Mock accuracy
            "model_path": f"models/{algorithm}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
        }
        
        self.local_models[algorithm] = model_info
        return model_info
    
    async def extract_knowledge(self, task="sentiment"):
        """Extract knowledge from trained models"""
        if not self.local_models:
            raise Exception("No trained models available")
        
        # Simulate knowledge extraction
        await asyncio.sleep(1)
        
        knowledge = {
            "task": task,
            "extracted_at": datetime.now().isoformat(),
            "insights": [
                "Positive sentiment dominates in Arabic news",
                "Negative sentiment correlates with economic topics",
                "Neutral sentiment is common in technical articles"
            ],
            "confidence": 0.78,
            "model_used": list(self.local_models.keys())[0]
        }
        
        return knowledge
    
    async def publish_contribution(self, contribution_type, data, signature=True):
        """Publish contribution to the network"""
        if not self.connected:
            raise Exception("Not connected to any topic")
        
        # Simulate publishing
        await asyncio.sleep(1)
        
        contribution = {
            "node_id": self.config.config["node_id"],
            "type": contribution_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "topic": self.current_topic,
            "signature": f"sig_{self.config.config['node_id']}_{datetime.now().timestamp()}" if signature else None
        }
        
        # Update rewards
        ledger = self.config.load_ledger()
        node_id = self.config.config["node_id"]
        
        if node_id not in ledger:
            ledger[node_id] = {"score": 0, "contributions": 0}
        
        reward = self.config.config["rewards"].get(contribution_type, 5)
        ledger[node_id]["score"] += reward
        ledger[node_id]["contributions"] += 1
        
        self.config.save_ledger(ledger)
        
        return contribution

# Global instances
config = P2PAIConfig()
node = P2PAINode(config)

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Verbose output / إخراج مفصل')
def cli(verbose):
    """P2P AI Decentralized System - نظام الذكاء الاصطناعي اللامركزي"""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

@cli.command()
@click.option('--topic', '-t', required=True, help='Topic to connect to / الموضوع للاتصال به')
def connect(topic):
    """Connect to a P2P topic / الاتصال بموضوع P2P"""
    click.echo(f"🔄 Connecting to topic: {topic} / الاتصال بالموضوع: {topic}")
    
    async def _connect():
        success = await node.connect_to_topic(topic)
        if success:
            click.echo(f"✅ Connected to topic: {topic}")
            click.echo(f"✅ تم الاتصال بالموضوع: {topic}")
        else:
            click.echo(f"❌ Failed to connect to topic: {topic}")
            click.echo(f"❌ فشل الاتصال بالموضوع: {topic}")
    
    asyncio.run(_connect())

@cli.command()
@click.option('--limit', '-l', default=100, help='Number of data points to fetch / عدد نقاط البيانات للحصول عليها')
def fetch_data(limit):
    """Fetch data from the network / جلب البيانات من الشبكة"""
    click.echo(f"📥 Fetching {limit} data points... / جلب {limit} نقطة بيانات...")
    
    async def _fetch():
        try:
            data = await node.fetch_data(limit)
            click.echo(f"✅ Fetched {len(data)} data points")
            click.echo(f"✅ تم جلب {len(data)} نقطة بيانات")
            
            # Show sample data
            if data:
                click.echo("\n📋 Sample data / بيانات تجريبية:")
                click.echo(f"   {data[0]['content'][:50]}...")
        except Exception as e:
            click.echo(f"❌ Error: {e}")
            click.echo(f"❌ خطأ: {e}")
    
    asyncio.run(_fetch())

@cli.command()
@click.option('--algorithm', '-a', default='bert', help='Algorithm to use / الخوارزمية للاستخدام')
@click.option('--epochs', '-e', default=3, help='Number of training epochs / عدد دورات التدريب')
def train(algorithm, epochs):
    """Train a local model / تدريب نموذج محلي"""
    click.echo(f"🤖 Training {algorithm} model for {epochs} epochs...")
    click.echo(f"🤖 تدريب نموذج {algorithm} لمدة {epochs} دورات...")
    
    async def _train():
        try:
            model_info = await node.train_model(algorithm, epochs)
            click.echo(f"✅ Training completed!")
            click.echo(f"✅ تم الانتهاء من التدريب!")
            click.echo(f"   Algorithm: {model_info['algorithm']}")
            click.echo(f"   Accuracy: {model_info['accuracy']:.2%}")
            click.echo(f"   Data size: {model_info['data_size']}")
        except Exception as e:
            click.echo(f"❌ Error: {e}")
            click.echo(f"❌ خطأ: {e}")
    
    asyncio.run(_train())

@cli.command()
@click.option('--task', '-t', default='sentiment', help='Knowledge extraction task / مهمة استخراج المعرفة')
def extract(task):
    """Extract knowledge from models / استخراج المعرفة من النماذج"""
    click.echo(f"🧠 Extracting knowledge for task: {task}")
    click.echo(f"🧠 استخراج المعرفة للمهمة: {task}")
    
    async def _extract():
        try:
            knowledge = await node.extract_knowledge(task)
            click.echo(f"✅ Knowledge extracted!")
            click.echo(f"✅ تم استخراج المعرفة!")
            click.echo(f"   Confidence: {knowledge['confidence']:.2%}")
            click.echo(f"   Insights: {len(knowledge['insights'])} found")
            
            for i, insight in enumerate(knowledge['insights'], 1):
                click.echo(f"   {i}. {insight}")
        except Exception as e:
            click.echo(f"❌ Error: {e}")
            click.echo(f"❌ خطأ: {e}")
    
    asyncio.run(_extract())

@cli.command()
@click.option('--type', '-t', required=True, help='Contribution type / نوع المساهمة')
@click.option('--signature/--no-signature', default=True, help='Sign the contribution / توقيع المساهمة')
def publish(type, signature):
    """Publish contribution to network / نشر المساهمة في الشبكة"""
    click.echo(f"📤 Publishing {type} contribution...")
    click.echo(f"📤 نشر مساهمة {type}...")
    
    async def _publish():
        try:
            # Mock data for publishing
            data = {
                "content": "Sample contribution data",
                "metadata": {"timestamp": datetime.now().isoformat()}
            }
            
            contribution = await node.publish_contribution(type, data, signature)
            click.echo(f"✅ Contribution published!")
            click.echo(f"✅ تم نشر المساهمة!")
            click.echo(f"   Node ID: {contribution['node_id']}")
            click.echo(f"   Topic: {contribution['topic']}")
            if signature:
                click.echo(f"   Signed: Yes")
        except Exception as e:
            click.echo(f"❌ Error: {e}")
            click.echo(f"❌ خطأ: {e}")
    
    asyncio.run(_publish())

@cli.command()
def leaderboard():
    """Show rewards leaderboard / عرض قائمة المكافآت"""
    ledger = config.load_ledger()
    
    if not ledger:
        click.echo("📊 No contributions yet / لا توجد مساهمات بعد")
        return
    
    click.echo("🏆 Rewards Leaderboard / قائمة المكافآت")
    click.echo("=" * 50)
    
    # Sort by score
    sorted_nodes = sorted(ledger.items(), key=lambda x: x[1]['score'], reverse=True)
    
    for i, (node_id, stats) in enumerate(sorted_nodes, 1):
        click.echo(f"{i:2d}. {node_id}")
        click.echo(f"    Score: {stats['score']} | Contributions: {stats['contributions']}")
        click.echo(f"    النقاط: {stats['score']} | المساهمات: {stats['contributions']}")

@cli.command()
def status():
    """Show current node status / عرض حالة العقدة الحالية"""
    click.echo("📊 Node Status / حالة العقدة")
    click.echo("=" * 30)
    click.echo(f"Node ID: {config.config['node_id']}")
    click.echo(f"Connected: {node.connected}")
    click.echo(f"Current Topic: {node.current_topic or 'None'}")
    click.echo(f"Local Data: {len(node.local_data)} items")
    click.echo(f"Trained Models: {len(node.local_models)}")
    
    # Show rewards
    ledger = config.load_ledger()
    node_stats = ledger.get(config.config['node_id'], {"score": 0, "contributions": 0})
    click.echo(f"Total Score: {node_stats['score']}")
    click.echo(f"Total Contributions: {node_stats['contributions']}")

@cli.command()
def help_ar():
    """Show help in Arabic / عرض المساعدة بالعربية"""
    help_text = """
🎯 نظام الذكاء الاصطناعي اللامركزي - المساعدة

الأوامر المتاحة:
  connect    - الاتصال بموضوع P2P
  fetch-data - جلب البيانات من الشبكة
  train      - تدريب نموذج محلي
  extract    - استخراج المعرفة من النماذج
  publish    - نشر المساهمة في الشبكة
  leaderboard- عرض قائمة المكافآت
  status     - عرض حالة العقدة
  help-ar    - عرض هذه المساعدة

أمثلة:
  p2p-ai connect --topic arabic_news
  p2p-ai fetch-data --limit 50
  p2p-ai train --algorithm bert --epochs 5
  p2p-ai extract --task sentiment
  p2p-ai publish --type data_contribution
  p2p-ai leaderboard
"""
    click.echo(help_text)

if __name__ == '__main__':
    cli() 