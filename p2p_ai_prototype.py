#!/usr/bin/env python3
"""
P2P AI Prototype - PyTorch + libp2p Implementation
نموذج أولي للنظام اللامركزي - PyTorch + libp2p
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from dataclasses import dataclass
import hashlib
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Message:
    """P2P message structure"""
    node_id: str
    message_type: str
    data: Any
    timestamp: str
    signature: Optional[str] = None

class SimpleBERT(nn.Module):
    """Simplified BERT-like model for text classification"""
    
    def __init__(self, vocab_size=10000, hidden_size=256, num_classes=3):
        super(SimpleBERT, self).__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.transformer = nn.TransformerEncoderLayer(
            d_model=hidden_size,
            nhead=8,
            dim_feedforward=1024,
            dropout=0.1
        )
        self.classifier = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, x):
        # x shape: (batch_size, seq_len)
        embedded = self.embedding(x)
        # Add positional encoding (simplified)
        embedded = embedded + self._get_positional_encoding(embedded.size(1), embedded.size(2))
        # Transformer layers
        transformed = self.transformer(embedded)
        # Global average pooling
        pooled = torch.mean(transformed, dim=1)
        pooled = self.dropout(pooled)
        # Classification
        output = self.classifier(pooled)
        return output
    
    def _get_positional_encoding(self, seq_len, hidden_size):
        """Simple positional encoding"""
        pos_encoding = torch.zeros(seq_len, hidden_size)
        for pos in range(seq_len):
            for i in range(hidden_size):
                if i % 2 == 0:
                    pos_encoding[pos, i] = np.sin(pos / (10000 ** (i / hidden_size)))
                else:
                    pos_encoding[pos, i] = np.cos(pos / (10000 ** ((i-1) / hidden_size)))
        return pos_encoding.unsqueeze(0)

class SimpleDataset(Dataset):
    """Simple dataset for text classification"""
    
    def __init__(self, texts, labels, tokenizer=None):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer or self._simple_tokenizer
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        # Simple tokenization (convert to indices)
        tokens = self.tokenizer(text)
        return torch.tensor(tokens, dtype=torch.long), torch.tensor(label, dtype=torch.long)
    
    def _simple_tokenizer(self, text):
        """Simple tokenizer that converts text to indices"""
        # This is a very simple tokenizer - in production you'd use a proper one
        words = text.lower().split()
        tokens = []
        for word in words:
            # Simple hash-based tokenization
            token_id = hash(word) % 10000
            tokens.append(token_id)
        
        # Pad or truncate to fixed length
        max_len = 128
        if len(tokens) > max_len:
            tokens = tokens[:max_len]
        else:
            tokens.extend([0] * (max_len - len(tokens)))
        
        return tokens

class P2PAIPrototype:
    """P2P AI Prototype with PyTorch models"""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.models = {}
        self.data = []
        self.peers = {}
        self.training_history = []
        
        # Initialize device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        
        # Create models directory
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
    
    async def create_model(self, model_type: str = "bert", **kwargs) -> Dict:
        """Create a new model"""
        try:
            if model_type == "bert":
                model = SimpleBERT(
                    vocab_size=kwargs.get('vocab_size', 10000),
                    hidden_size=kwargs.get('hidden_size', 256),
                    num_classes=kwargs.get('num_classes', 3)
                )
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            model = model.to(self.device)
            model_id = f"{model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self.models[model_id] = {
                'model': model,
                'type': model_type,
                'created_at': datetime.now().isoformat(),
                'parameters': kwargs
            }
            
            logger.info(f"Created model: {model_id}")
            return {
                'model_id': model_id,
                'type': model_type,
                'created_at': datetime.now().isoformat(),
                'device': str(self.device)
            }
        
        except Exception as e:
            logger.error(f"Error creating model: {e}")
            raise
    
    async def train_model(self, model_id: str, texts: List[str], labels: List[int], 
                         epochs: int = 3, batch_size: int = 32) -> Dict:
        """Train a model"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        try:
            model_info = self.models[model_id]
            model = model_info['model']
            
            # Create dataset and dataloader
            dataset = SimpleDataset(texts, labels)
            dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
            
            # Setup training
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(model.parameters(), lr=0.001)
            
            # Training loop
            model.train()
            training_history = []
            
            for epoch in range(epochs):
                epoch_loss = 0.0
                correct = 0
                total = 0
                
                for batch_idx, (inputs, targets) in enumerate(dataloader):
                    inputs, targets = inputs.to(self.device), targets.to(self.device)
                    
                    optimizer.zero_grad()
                    outputs = model(inputs)
                    loss = criterion(outputs, targets)
                    loss.backward()
                    optimizer.step()
                    
                    epoch_loss += loss.item()
                    _, predicted = outputs.max(1)
                    total += targets.size(0)
                    correct += predicted.eq(targets).sum().item()
                
                accuracy = 100. * correct / total
                avg_loss = epoch_loss / len(dataloader)
                
                training_history.append({
                    'epoch': epoch + 1,
                    'loss': avg_loss,
                    'accuracy': accuracy
                })
                
                logger.info(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%")
            
            # Update model info
            model_info['trained_at'] = datetime.now().isoformat()
            model_info['training_history'] = training_history
            model_info['final_accuracy'] = accuracy
            
            # Save model
            await self.save_model(model_id)
            
            return {
                'model_id': model_id,
                'epochs': epochs,
                'final_accuracy': accuracy,
                'final_loss': avg_loss,
                'training_history': training_history
            }
        
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise
    
    async def predict(self, model_id: str, texts: List[str]) -> List[Dict]:
        """Make predictions using a trained model"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        try:
            model_info = self.models[model_id]
            model = model_info['model']
            
            model.eval()
            predictions = []
            
            with torch.no_grad():
                for text in texts:
                    # Tokenize text
                    dataset = SimpleDataset([text], [0])  # Dummy label
                    tokens, _ = dataset[0]
                    tokens = tokens.unsqueeze(0).to(self.device)
                    
                    # Make prediction
                    output = model(tokens)
                    probabilities = torch.softmax(output, dim=1)
                    predicted_class = torch.argmax(probabilities, dim=1).item()
                    confidence = probabilities[0][predicted_class].item()
                    
                    predictions.append({
                        'text': text,
                        'predicted_class': predicted_class,
                        'confidence': confidence,
                        'probabilities': probabilities[0].cpu().numpy().tolist()
                    })
            
            return predictions
        
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            raise
    
    async def save_model(self, model_id: str) -> str:
        """Save model to disk"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        try:
            model_info = self.models[model_id]
            model = model_info['model']
            
            # Save model state
            model_path = self.models_dir / f"{model_id}.pth"
            torch.save(model.state_dict(), model_path)
            
            # Save model info
            info_path = self.models_dir / f"{model_id}_info.json"
            info_to_save = {k: v for k, v in model_info.items() if k != 'model'}
            
            with open(info_path, 'w') as f:
                json.dump(info_to_save, f, indent=2)
            
            logger.info(f"Model saved: {model_path}")
            return str(model_path)
        
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise
    
    async def load_model(self, model_id: str) -> bool:
        """Load model from disk"""
        try:
            model_path = self.models_dir / f"{model_id}.pth"
            info_path = self.models_dir / f"{model_id}_info.json"
            
            if not model_path.exists() or not info_path.exists():
                return False
            
            # Load model info
            with open(info_path, 'r') as f:
                model_info = json.load(f)
            
            # Create model
            if model_info['type'] == 'bert':
                model = SimpleBERT(**model_info['parameters'])
            else:
                raise ValueError(f"Unknown model type: {model_info['type']}")
            
            # Load state
            model.load_state_dict(torch.load(model_path, map_location=self.device))
            model = model.to(self.device)
            
            # Update models dict
            model_info['model'] = model
            self.models[model_id] = model_info
            
            logger.info(f"Model loaded: {model_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    async def add_data(self, texts: List[str], labels: List[int]) -> int:
        """Add training data"""
        for text, label in zip(texts, labels):
            self.data.append({
                'text': text,
                'label': label,
                'added_at': datetime.now().isoformat()
            })
        
        logger.info(f"Added {len(texts)} data points")
        return len(self.data)
    
    async def get_model_info(self, model_id: str) -> Dict:
        """Get information about a model"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model_info = self.models[model_id].copy()
        model_info.pop('model', None)  # Remove the actual model object
        return model_info
    
    async def list_models(self) -> List[Dict]:
        """List all available models"""
        models_info = []
        for model_id, model_info in self.models.items():
            info = {
                'model_id': model_id,
                'type': model_info['type'],
                'created_at': model_info['created_at'],
                'trained_at': model_info.get('trained_at'),
                'final_accuracy': model_info.get('final_accuracy')
            }
            models_info.append(info)
        
        return models_info
    
    def _create_signature(self, data: str) -> str:
        """Create a simple signature for data"""
        # In production, use proper cryptographic signatures
        signature_data = f"{self.node_id}:{data}:{datetime.now().timestamp()}"
        return hashlib.sha256(signature_data.encode()).hexdigest()[:16]
    
    async def create_message(self, message_type: str, data: Any) -> Message:
        """Create a P2P message"""
        signature = self._create_signature(str(data))
        return Message(
            node_id=self.node_id,
            message_type=message_type,
            data=data,
            timestamp=datetime.now().isoformat(),
            signature=signature
        )

# Example usage and testing
async def main():
    """Example usage of the P2P AI prototype"""
    print("🚀 Starting P2P AI Prototype...")
    
    # Create prototype instance
    prototype = P2PAIPrototype("node_123")
    
    # Sample Arabic text data
    arabic_texts = [
        "هذا نص إيجابي جميل",
        "هذا نص سلبي سيء",
        "هذا نص محايد عادي",
        "أحب هذا المنتج كثيراً",
        "لا أحب هذا المنتج إطلاقاً",
        "هذا المنتج مقبول"
    ]
    
    # Labels: 0=negative, 1=neutral, 2=positive
    labels = [2, 0, 1, 2, 0, 1]
    
    try:
        # Add data
        await prototype.add_data(arabic_texts, labels)
        print(f"✅ Added {len(arabic_texts)} data points")
        
        # Create model
        model_info = await prototype.create_model("bert", num_classes=3)
        model_id = model_info['model_id']
        print(f"✅ Created model: {model_id}")
        
        # Train model
        training_result = await prototype.train_model(model_id, arabic_texts, labels, epochs=5)
        print(f"✅ Training completed - Accuracy: {training_result['final_accuracy']:.2f}%")
        
        # Make predictions
        test_texts = ["أحب هذا كثيراً", "لا أحب هذا", "هذا مقبول"]
        predictions = await prototype.predict(model_id, test_texts)
        
        print("\n📊 Predictions:")
        for pred in predictions:
            sentiment = ["سلبي", "محايد", "إيجابي"][pred['predicted_class']]
            print(f"   '{pred['text']}' -> {sentiment} (confidence: {pred['confidence']:.2f})")
        
        # Save model
        await prototype.save_model(model_id)
        print(f"✅ Model saved")
        
        # List models
        models = await prototype.list_models()
        print(f"\n📋 Available models: {len(models)}")
        for model in models:
            print(f"   {model['model_id']} - {model['type']} - Accuracy: {model.get('final_accuracy', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 