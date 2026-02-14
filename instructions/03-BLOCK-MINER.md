# 03-BLOCK-MINER - ブロック構造とマイニング機能

## 指示タイプ
**FIRST_CODING** - コア機能の新規実装

## 目的
ブロックチェーンの中核となる「ブロック」クラスと、Proof of Work による「マイニング」機能を実装する。

---

## 前提条件

- `02-PARTICIPANTS-TRANSACTION.md` が完了していること
- `transaction.py` が動作すること

---

## 実装ファイル

### 1. src/simple_blockchain/block.py

**責務:** ブロックの構造定義とハッシュ計算

**実装するクラス:**

#### `class Block`

**属性:**
- `index`: int - ブロック番号（0から始まる）
- `timestamp`: int - 作成時刻（UNIXタイム）
- `transactions`: list[dict] - 含まれるトランザクション
- `previous_hash`: str - 前のブロックのハッシュ
- `nonce`: int - マイニングで見つける値
- `hash`: str - このブロックのハッシュ

**実装例:**

```python
import hashlib
import json
import time
from typing import Optional

class Block:
    """
    ブロックチェーンの1ブロックを表すクラス
    
    Attributes:
        index: ブロック番号（0から始まる）
        timestamp: 作成時刻（UNIXタイム）
        transactions: 含まれるトランザクションのリスト
        previous_hash: 前のブロックのハッシュ値
        nonce: Proof of Workで見つける値
        hash: このブロックのハッシュ値
    """
    
    def __init__(
        self,
        index: int,
        transactions: list[dict],
        previous_hash: str,
        timestamp: Optional[int] = None
    ):
        """
        ブロックを初期化
        
        Args:
            index: ブロック番号
            transactions: トランザクションリスト
            previous_hash: 前のブロックのハッシュ
            timestamp: タイムスタンプ（Noneの場合は現在時刻）
        """
        self.index = index
        self.timestamp = timestamp if timestamp is not None else int(time.time())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0  # マイニング前は0
        self.hash = ""  # マイニング前は空
    
    def compute_hash(self) -> str:
        """
        ブロックのハッシュを計算
        
        nonce以外のすべてのデータをJSON化してSHA256でハッシュ化する
        
        Returns:
            str: 16進数表現のハッシュ値
        """
        # ブロックの内容を辞書にまとめる
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        
        # JSON文字列に変換（キーの順序を固定）
        block_string = json.dumps(block_data, sort_keys=True)
        
        # SHA256でハッシュ化
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> dict:
        """
        ブロックを辞書形式に変換（JSON保存用）
        
        Returns:
            dict: ブロックデータ
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Block':
        """
        辞書形式からBlockオブジェクトを復元
        
        Args:
            data: ブロックデータの辞書
            
        Returns:
            Block: 復元されたBlockオブジェクト
        """
        block = Block(
            index=data["index"],
            transactions=data["transactions"],
            previous_hash=data["previous_hash"],
            timestamp=data["timestamp"]
        )
        block.nonce = data["nonce"]
        block.hash = data["hash"]
        return block
    
    def __str__(self) -> str:
        """
        ブロックの文字列表現
        """
        return (
            f"Block #{self.index}\n"
            f"  Timestamp: {self.timestamp}\n"
            f"  Transactions: {len(self.transactions)}\n"
            f"  Previous Hash: {self.previous_hash[:16]}...\n"
            f"  Nonce: {self.nonce}\n"
            f"  Hash: {self.hash[:16]}..."
        )
```

---

### 2. src/simple_blockchain/miner.py

**責務:** Proof of Work によるマイニング処理

**実装する関数:**

#### `mine(block: Block, difficulty: str = "00") -> Block`

**処理内容:**
1. difficulty（例: "00"）で始まるハッシュを見つけるまでnonceを増やす
2. 1000回ごとに進行状況を表示
3. 見つかったらブロックにハッシュを設定して返す

**実装例:**

```python
from .block import Block

def mine(block: Block, difficulty: str = "00") -> Block:
    """
    Proof of Work でブロックをマイニング
    
    難易度条件を満たすハッシュが見つかるまでnonceを増やし続ける
    
    Args:
        block: マイニング対象のブロック
        difficulty: ハッシュの先頭一致条件（例: "00"）
        
    Returns:
        Block: マイニング完了したブロック
    """
    print("\n" + "="*60)
    print(f" マイニング開始: Block #{block.index}")
    print("="*60)
    print(f"難易度: ハッシュが '{difficulty}' で始まる必要あり")
    print(f"トランザクション数: {len(block.transactions)}\n")
    
    # nonceを0から順に試す
    block.nonce = 0
    
    while True:
        # ハッシュを計算
        computed_hash = block.compute_hash()
        
        # 進行状況表示（1000回ごと）
        if block.nonce % 1000 == 0:
            print(f"試行回数: {block.nonce:,} | 現在のハッシュ: {computed_hash[:32]}...")
        
        # 難易度条件をチェック
        if computed_hash.startswith(difficulty):
            # 成功！
            block.hash = computed_hash
            print("\n" + "="*60)
            print("✅ マイニング成功！")
            print("="*60)
            print(f"Nonce: {block.nonce:,}")
            print(f"Hash: {block.hash}")
            print(f"試行回数: {block.nonce + 1:,}")
            print("="*60 + "\n")
            return block
        
        # 次のnonceを試す
        block.nonce += 1
        
        # 安全装置（無限ループ防止）
        if block.nonce > 10_000_000:
            print("⚠️  警告: 試行回数が1000万を超えました")
            print("難易度が高すぎる可能性があります")
            # それでも続行する場合はこの行を削除
            break
    
    return block


def create_genesis_block() -> Block:
    """
    ジェネシスブロック（最初のブロック）を作成
    
    Returns:
        Block: ジェネシスブロック
    """
    print("\n" + "="*60)
    print(" ジェネシスブロック作成")
    print("="*60)
    
    genesis = Block(
        index=0,
        transactions=[{
            "from": "SYSTEM",
            "to": "NETWORK",
            "amount": 0,
            "timestamp": 0
        }],
        previous_hash="0" * 64  # 64文字の0
    )
    
    # ジェネシスブロックは難易度低めでマイニング
    genesis = mine(genesis, difficulty="0")
    
    print("✅ ジェネシスブロック作成完了")
    print("="*60 + "\n")
    
    return genesis
```

---

## コーディングのポイント

### 1. ハッシュ計算の注意点

```python
# ❌ 間違い: hashは含めない（循環参照になる）
block_data = {
    "index": self.index,
    "hash": self.hash,  # これはNG
    ...
}

# ✅ 正しい: hash以外のデータでハッシュを計算
block_data = {
    "index": self.index,
    "nonce": self.nonce,
    ...
}
```

### 2. JSON のキー順序

```python
# ✅ sort_keys=True で順序を固定
json.dumps(block_data, sort_keys=True)

# なぜ？ キーの順序が変わるとハッシュも変わってしまうため
```

### 3. 難易度の意味

```python
difficulty = "00"   # ハッシュが "00" で始まる（1/256の確率）
difficulty = "000"  # ハッシュが "000" で始まる（1/4096の確率）
difficulty = "0"    # ハッシュが "0" で始まる（1/16の確率）
```

---

## テスト方法

### block.py のテスト

```python
# ファイル末尾に追加
if __name__ == "__main__":
    print("=== ブロックモジュール テスト ===\n")
    
    # サンプルトランザクション
    transactions = [
        {"from": "Alice", "to": "Bob", "amount": 100, "timestamp": 1234567890}
    ]
    
    # ブロック作成
    block = Block(
        index=1,
        transactions=transactions,
        previous_hash="0" * 64
    )
    
    print(block)
    print("\nハッシュ計算テスト:")
    
    # nonce=0でハッシュ計算
    hash1 = block.compute_hash()
    print(f"Nonce=0: {hash1}")
    
    # nonce=1でハッシュ計算
    block.nonce = 1
    hash2 = block.compute_hash()
    print(f"Nonce=1: {hash2}")
    
    # ハッシュが異なることを確認
    print(f"\nハッシュが異なる: {hash1 != hash2}")
    
    # JSON変換テスト
    block_dict = block.to_dict()
    print(f"\nJSON変換: {block_dict}")
    
    # 復元テスト
    restored_block = Block.from_dict(block_dict)
    print(f"復元成功: {restored_block.index == block.index}")
```

実行:
```bash
python src/simple_blockchain/block.py
```

### miner.py のテスト

```python
# ファイル末尾に追加
if __name__ == "__main__":
    import sys
    sys.path.insert(0, "src")
    
    from simple_blockchain.block import Block
    
    print("=== マイナーモジュール テスト ===\n")
    
    # ジェネシスブロック作成
    genesis = create_genesis_block()
    print(f"ジェネシスブロック: {genesis}\n")
    
    # 通常ブロックのマイニング
    transactions = [
        {"from": "Alice", "to": "Bob", "amount": 50, "timestamp": 1234567890},
        {"from": "Bob", "to": "Carol", "amount": 30, "timestamp": 1234567891}
    ]
    
    block = Block(
        index=1,
        transactions=transactions,
        previous_hash=genesis.hash
    )
    
    # 難易度 "00" でマイニング
    mined_block = mine(block, difficulty="00")
    print(f"\nマイニング結果:\n{mined_block}")
```

実行:
```bash
python src/simple_blockchain/miner.py
```

---

## 完了条件

✅ `Block` クラスが実装されている  
✅ `compute_hash()` が正しくハッシュを計算する  
✅ `to_dict()` と `from_dict()` で変換・復元できる  
✅ `mine()` 関数が動作する  
✅ 進行状況が表示される  
✅ テストコードが動作する

---

## 動作確認例

```bash
# ブロックのテスト
python src/simple_blockchain/block.py

# マイニングのテスト（時間がかかる場合あり）
python src/simple_blockchain/miner.py

# 出力例:
# 試行回数: 0 | 現在のハッシュ: 3a7bd3e2987a3c5b...
# 試行回数: 1,000 | 現在のハッシュ: 8f2e9c1d4b5a7e3f...
# ...
# ✅ マイニング成功！
# Nonce: 12,345
# Hash: 00a3f5e8c2d1b9e7...
```

---

## トラブルシューティング

**Q: マイニングが終わらない**  
A: difficulty を "0" に変更してテスト

**Q: ハッシュが毎回変わる**  
A: `timestamp` が変わっている可能性。テスト時は固定値を使用

**Q: import エラー**  
A: `from .block import Block` が使えない場合は絶対importに変更

---

## 発展課題（任意）

1. difficulty を変更して試行回数の違いを観察
2. トランザクション数を変えて動作確認
3. ハッシュ値の先頭2文字を表示して視覚化

---

## 次のステップ

実装とテストが完了したら:

```
Please follow the instructions in ./instructions/04-BLOCKCHAIN.md
```
