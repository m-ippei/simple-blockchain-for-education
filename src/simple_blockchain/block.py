"""
ブロックモジュール

ブロックチェーンの1ブロックを表すクラスを定義する。
- ブロックの構造定義
- ハッシュ計算
- JSON変換・復元
"""

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
        timestamp: Optional[int] = None,
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
            "nonce": self.nonce,
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
            "hash": self.hash,
        }

    @staticmethod
    def from_dict(data: dict) -> "Block":
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
            timestamp=data["timestamp"],
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


if __name__ == "__main__":
    print("=== ブロックモジュール テスト ===\n")

    # サンプルトランザクション
    transactions = [
        {"from": "Alice", "to": "Bob", "amount": 100, "timestamp": 1234567890}
    ]

    # ブロック作成
    block = Block(index=1, transactions=transactions, previous_hash="0" * 64)

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
