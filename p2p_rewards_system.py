#!/usr/bin/env python3
"""
P2P Rewards System - Token and Reputation Management
نظام المكافآت اللامركزي - إدارة التوكنات والسمعة
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContributionType(Enum):
    """Types of contributions that earn rewards"""
    DATA_CONTRIBUTION = "data_contribution"
    MODEL_TRAINING = "model_training"
    KNOWLEDGE_EXTRACTION = "knowledge_extraction"
    VALIDATION = "validation"
    PEER_REVIEW = "peer_review"
    NETWORK_MAINTENANCE = "network_maintenance"

class RewardTier(Enum):
    """Reward tiers based on contribution quality"""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"

@dataclass
class Contribution:
    """Contribution record"""
    node_id: str
    contribution_type: str
    data_hash: str
    timestamp: str
    reward_amount: float
    quality_score: float
    verified: bool = False
    signature: Optional[str] = None

@dataclass
class Reward:
    """Reward record"""
    node_id: str
    amount: float
    contribution_type: str
    timestamp: str
    transaction_hash: str
    status: str = "pending"

@dataclass
class Reputation:
    """Reputation information"""
    node_id: str
    total_score: float
    contribution_count: int
    last_contribution: str
    tier: str
    trust_level: float

class P2PRewardsSystem:
    """Manages rewards and reputation in the P2P network"""
    
    def __init__(self, config_dir: str = ".p2p_rewards"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.ledger_file = self.config_dir / "ledger.json"
        self.contributions_file = self.config_dir / "contributions.json"
        self.reputation_file = self.config_dir / "reputation.json"
        self.rewards_file = self.config_dir / "rewards.json"
        
        # Load or create databases
        self.ledger = self._load_ledger()
        self.contributions = self._load_contributions()
        self.reputation = self._load_reputation()
        self.rewards = self._load_rewards()
        
        # Reward multipliers based on contribution type
        self.reward_multipliers = {
            ContributionType.DATA_CONTRIBUTION.value: 1.0,
            ContributionType.MODEL_TRAINING.value: 2.0,
            ContributionType.KNOWLEDGE_EXTRACTION.value: 3.0,
            ContributionType.VALIDATION.value: 1.5,
            ContributionType.PEER_REVIEW.value: 2.5,
            ContributionType.NETWORK_MAINTENANCE.value: 1.0
        }
        
        # Base reward amounts
        self.base_rewards = {
            ContributionType.DATA_CONTRIBUTION.value: 5.0,
            ContributionType.MODEL_TRAINING.value: 10.0,
            ContributionType.KNOWLEDGE_EXTRACTION.value: 15.0,
            ContributionType.VALIDATION.value: 7.5,
            ContributionType.PEER_REVIEW.value: 12.5,
            ContributionType.NETWORK_MAINTENANCE.value: 5.0
        }
        
        # Quality thresholds for different tiers
        self.quality_thresholds = {
            RewardTier.BRONZE.value: 0.0,
            RewardTier.SILVER.value: 0.6,
            RewardTier.GOLD.value: 0.8,
            RewardTier.PLATINUM.value: 0.95
        }
        
        logger.info("Rewards system initialized")
    
    def _load_ledger(self) -> Dict[str, Dict]:
        """Load ledger from file"""
        if self.ledger_file.exists():
            with open(self.ledger_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_ledger(self):
        """Save ledger to file"""
        with open(self.ledger_file, 'w', encoding='utf-8') as f:
            json.dump(self.ledger, f, indent=2, ensure_ascii=False)
    
    def _load_contributions(self) -> List[Dict]:
        """Load contributions from file"""
        if self.contributions_file.exists():
            with open(self.contributions_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_contributions(self):
        """Save contributions to file"""
        with open(self.contributions_file, 'w', encoding='utf-8') as f:
            json.dump(self.contributions, f, indent=2, ensure_ascii=False)
    
    def _load_reputation(self) -> Dict[str, Dict]:
        """Load reputation from file"""
        if self.reputation_file.exists():
            with open(self.reputation_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_reputation(self):
        """Save reputation to file"""
        with open(self.reputation_file, 'w', encoding='utf-8') as f:
            json.dump(self.reputation, f, indent=2, ensure_ascii=False)
    
    def _load_rewards(self) -> List[Dict]:
        """Load rewards from file"""
        if self.rewards_file.exists():
            with open(self.rewards_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_rewards(self):
        """Save rewards to file"""
        with open(self.rewards_file, 'w', encoding='utf-8') as f:
            json.dump(self.rewards, f, indent=2, ensure_ascii=False)
    
    def _calculate_reward(self, contribution_type: str, quality_score: float) -> float:
        """Calculate reward amount based on contribution type and quality"""
        base_reward = self.base_rewards.get(contribution_type, 5.0)
        multiplier = self.reward_multipliers.get(contribution_type, 1.0)
        
        # Quality bonus (0-50% extra)
        quality_bonus = quality_score * 0.5
        
        # Calculate final reward
        reward = base_reward * multiplier * (1 + quality_bonus)
        
        return round(reward, 2)
    
    def _determine_tier(self, total_score: float) -> str:
        """Determine reward tier based on total score"""
        if total_score >= self.quality_thresholds[RewardTier.PLATINUM.value]:
            return RewardTier.PLATINUM.value
        elif total_score >= self.quality_thresholds[RewardTier.GOLD.value]:
            return RewardTier.GOLD.value
        elif total_score >= self.quality_thresholds[RewardTier.SILVER.value]:
            return RewardTier.SILVER.value
        else:
            return RewardTier.BRONZE.value
    
    def _calculate_trust_level(self, node_id: str) -> float:
        """Calculate trust level based on reputation and contributions"""
        if node_id not in self.reputation:
            return 0.0
        
        rep = self.reputation[node_id]
        
        # Base trust from reputation score
        trust = min(rep['total_score'] / 100.0, 1.0)
        
        # Bonus for high contribution count
        if rep['contribution_count'] > 50:
            trust += 0.1
        elif rep['contribution_count'] > 20:
            trust += 0.05
        
        # Bonus for high tier
        tier_bonus = {
            RewardTier.BRONZE.value: 0.0,
            RewardTier.SILVER.value: 0.1,
            RewardTier.GOLD.value: 0.2,
            RewardTier.PLATINUM.value: 0.3
        }
        trust += tier_bonus.get(rep['tier'], 0.0)
        
        return min(trust, 1.0)
    
    def record_contribution(self, node_id: str, contribution_type: str, 
                          data_hash: str, quality_score: float = 0.5, 
                          signature: str = None) -> Dict:
        """Record a new contribution and calculate rewards"""
        try:
            # Validate contribution type
            if contribution_type not in [ct.value for ct in ContributionType]:
                raise ValueError(f"Invalid contribution type: {contribution_type}")
            
            # Calculate reward
            reward_amount = self._calculate_reward(contribution_type, quality_score)
            
            # Create contribution record
            contribution = Contribution(
                node_id=node_id,
                contribution_type=contribution_type,
                data_hash=data_hash,
                timestamp=datetime.now().isoformat(),
                reward_amount=reward_amount,
                quality_score=quality_score,
                signature=signature
            )
            
            # Add to contributions list
            self.contributions.append(asdict(contribution))
            self._save_contributions()
            
            # Update ledger
            if node_id not in self.ledger:
                self.ledger[node_id] = {
                    "total_tokens": 0.0,
                    "total_contributions": 0,
                    "last_activity": datetime.now().isoformat()
                }
            
            self.ledger[node_id]["total_tokens"] += reward_amount
            self.ledger[node_id]["total_contributions"] += 1
            self.ledger[node_id]["last_activity"] = datetime.now().isoformat()
            self._save_ledger()
            
            # Update reputation
            self._update_reputation(node_id, quality_score, contribution_type)
            
            # Create reward record
            transaction_hash = self._create_transaction_hash(node_id, reward_amount, data_hash)
            reward = Reward(
                node_id=node_id,
                amount=reward_amount,
                contribution_type=contribution_type,
                timestamp=datetime.now().isoformat(),
                transaction_hash=transaction_hash,
                status="completed"
            )
            
            self.rewards.append(asdict(reward))
            self._save_rewards()
            
            logger.info(f"Contribution recorded for {node_id}: {contribution_type} - {reward_amount} tokens")
            
            return {
                "contribution_id": len(self.contributions),
                "reward_amount": reward_amount,
                "transaction_hash": transaction_hash,
                "new_balance": self.ledger[node_id]["total_tokens"]
            }
        
        except Exception as e:
            logger.error(f"Error recording contribution: {e}")
            raise
    
    def _update_reputation(self, node_id: str, quality_score: float, contribution_type: str):
        """Update node reputation"""
        if node_id not in self.reputation:
            self.reputation[node_id] = {
                "total_score": 0.0,
                "contribution_count": 0,
                "last_contribution": datetime.now().isoformat(),
                "tier": RewardTier.BRONZE.value,
                "trust_level": 0.0
            }
        
        rep = self.reputation[node_id]
        
        # Update scores
        rep["total_score"] = (rep["total_score"] * rep["contribution_count"] + quality_score) / (rep["contribution_count"] + 1)
        rep["contribution_count"] += 1
        rep["last_contribution"] = datetime.now().isoformat()
        
        # Update tier
        rep["tier"] = self._determine_tier(rep["total_score"])
        
        # Update trust level
        rep["trust_level"] = self._calculate_trust_level(node_id)
        
        self._save_reputation()
    
    def _create_transaction_hash(self, node_id: str, amount: float, data_hash: str) -> str:
        """Create a unique transaction hash"""
        transaction_data = f"{node_id}:{amount}:{data_hash}:{datetime.now().timestamp()}"
        return hashlib.sha256(transaction_data.encode()).hexdigest()
    
    def get_balance(self, node_id: str) -> float:
        """Get current token balance for a node"""
        return self.ledger.get(node_id, {}).get("total_tokens", 0.0)
    
    def get_reputation(self, node_id: str) -> Optional[Dict]:
        """Get reputation information for a node"""
        if node_id not in self.reputation:
            return None
        
        return self.reputation[node_id].copy()
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top contributors leaderboard"""
        # Sort by total tokens
        sorted_nodes = sorted(
            self.ledger.items(),
            key=lambda x: x[1]["total_tokens"],
            reverse=True
        )
        
        leaderboard = []
        for i, (node_id, data) in enumerate(sorted_nodes[:limit], 1):
            reputation = self.reputation.get(node_id, {})
            entry = {
                "rank": i,
                "node_id": node_id,
                "total_tokens": data["total_tokens"],
                "contributions": data["total_contributions"],
                "tier": reputation.get("tier", RewardTier.BRONZE.value),
                "trust_level": reputation.get("trust_level", 0.0)
            }
            leaderboard.append(entry)
        
        return leaderboard
    
    def get_contribution_history(self, node_id: str, limit: int = 20) -> List[Dict]:
        """Get contribution history for a node"""
        node_contributions = [
            c for c in self.contributions 
            if c["node_id"] == node_id
        ]
        
        # Sort by timestamp (newest first)
        sorted_contributions = sorted(
            node_contributions,
            key=lambda x: x["timestamp"],
            reverse=True
        )
        
        return sorted_contributions[:limit]
    
    def transfer_tokens(self, from_node: str, to_node: str, amount: float) -> bool:
        """Transfer tokens between nodes"""
        try:
            if from_node not in self.ledger:
                raise ValueError(f"Source node {from_node} not found")
            
            if self.ledger[from_node]["total_tokens"] < amount:
                raise ValueError(f"Insufficient balance: {self.ledger[from_node]['total_tokens']}")
            
            # Deduct from source
            self.ledger[from_node]["total_tokens"] -= amount
            
            # Add to destination
            if to_node not in self.ledger:
                self.ledger[to_node] = {
                    "total_tokens": 0.0,
                    "total_contributions": 0,
                    "last_activity": datetime.now().isoformat()
                }
            
            self.ledger[to_node]["total_tokens"] += amount
            self.ledger[to_node]["last_activity"] = datetime.now().isoformat()
            
            self._save_ledger()
            
            logger.info(f"Transferred {amount} tokens from {from_node} to {to_node}")
            return True
        
        except Exception as e:
            logger.error(f"Error transferring tokens: {e}")
            return False
    
    def get_network_stats(self) -> Dict:
        """Get network-wide statistics"""
        total_nodes = len(self.ledger)
        total_tokens = sum(data["total_tokens"] for data in self.ledger.values())
        total_contributions = sum(data["total_contributions"] for data in self.ledger.values())
        
        # Calculate tier distribution
        tier_distribution = {}
        for rep in self.reputation.values():
            tier = rep.get("tier", RewardTier.BRONZE.value)
            tier_distribution[tier] = tier_distribution.get(tier, 0) + 1
        
        return {
            "total_nodes": total_nodes,
            "total_tokens": total_tokens,
            "total_contributions": total_contributions,
            "average_tokens_per_node": total_tokens / total_nodes if total_nodes > 0 else 0,
            "tier_distribution": tier_distribution,
            "active_nodes_24h": self._count_active_nodes(hours=24),
            "active_nodes_7d": self._count_active_nodes(hours=168)
        }
    
    def _count_active_nodes(self, hours: int) -> int:
        """Count nodes active in the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        active_count = 0
        
        for data in self.ledger.values():
            last_activity = datetime.fromisoformat(data["last_activity"])
            if last_activity > cutoff_time:
                active_count += 1
        
        return active_count
    
    def validate_contribution(self, contribution_id: int, validator_node: str, 
                            is_valid: bool, feedback: str = "") -> bool:
        """Validate a contribution (peer review)"""
        try:
            if contribution_id >= len(self.contributions):
                raise ValueError(f"Invalid contribution ID: {contribution_id}")
            
            contribution = self.contributions[contribution_id]
            
            if is_valid:
                # Mark as verified
                contribution["verified"] = True
                
                # Give bonus to original contributor
                bonus = contribution["reward_amount"] * 0.1  # 10% bonus
                self.ledger[contribution["node_id"]]["total_tokens"] += bonus
                
                # Reward validator
                validator_reward = 2.0  # Base reward for validation
                if validator_node not in self.ledger:
                    self.ledger[validator_node] = {
                        "total_tokens": 0.0,
                        "total_contributions": 0,
                        "last_activity": datetime.now().isoformat()
                    }
                
                self.ledger[validator_node]["total_tokens"] += validator_reward
                self.ledger[validator_node]["total_contributions"] += 1
                
                # Record validation as contribution
                self.record_contribution(
                    validator_node,
                    ContributionType.VALIDATION.value,
                    f"validation_{contribution_id}",
                    quality_score=0.8
                )
                
                logger.info(f"Contribution {contribution_id} validated by {validator_node}")
            else:
                # Penalize invalid contribution
                penalty = contribution["reward_amount"] * 0.5  # 50% penalty
                self.ledger[contribution["node_id"]]["total_tokens"] -= penalty
                
                logger.warning(f"Contribution {contribution_id} marked as invalid by {validator_node}")
            
            self._save_contributions()
            self._save_ledger()
            
            return True
        
        except Exception as e:
            logger.error(f"Error validating contribution: {e}")
            return False

# Example usage and testing
def main():
    """Test the rewards system"""
    print("💰 Testing P2P Rewards System...")
    
    # Create rewards system
    rewards_system = P2PRewardsSystem()
    
    # Test contributions
    test_nodes = ["node_123", "node_456", "node_789"]
    
    for i, node_id in enumerate(test_nodes):
        # Record different types of contributions
        contribution_types = [
            ContributionType.DATA_CONTRIBUTION.value,
            ContributionType.MODEL_TRAINING.value,
            ContributionType.KNOWLEDGE_EXTRACTION.value
        ]
        
        for j, contrib_type in enumerate(contribution_types):
            data_hash = f"data_{node_id}_{i}_{j}"
            quality_score = 0.7 + (i * 0.1) + (j * 0.05)  # Varying quality
            
            result = rewards_system.record_contribution(
                node_id, contrib_type, data_hash, quality_score
            )
            
            print(f"✅ {node_id}: {contrib_type} - {result['reward_amount']} tokens")
    
    # Show leaderboard
    print("\n🏆 Leaderboard:")
    leaderboard = rewards_system.get_leaderboard(5)
    for entry in leaderboard:
        print(f"   {entry['rank']}. {entry['node_id']} - {entry['total_tokens']} tokens ({entry['tier']})")
    
    # Show network stats
    print("\n📊 Network Statistics:")
    stats = rewards_system.get_network_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test token transfer
    print(f"\n💸 Testing token transfer...")
    transfer_success = rewards_system.transfer_tokens("node_123", "node_456", 10.0)
    print(f"   Transfer result: {'SUCCESS' if transfer_success else 'FAILED'}")
    
    # Show updated balances
    for node_id in test_nodes:
        balance = rewards_system.get_balance(node_id)
        reputation = rewards_system.get_reputation(node_id)
        print(f"   {node_id}: {balance} tokens, Tier: {reputation['tier'] if reputation else 'N/A'}")
    
    print("\n🎉 Rewards system test completed!")

if __name__ == "__main__":
    main() 