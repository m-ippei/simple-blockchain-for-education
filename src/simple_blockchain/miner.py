"""
マイナーモジュール

Proof of Workによるブロックのマイニング処理を行う。
- 難易度に応じたハッシュ探索
- マイニング進行状況の表示
- ジェネシスブロックの作成
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.simple_blockchain.block import Block


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
    print("\n" + "=" * 60)
    print(f" マイニング開始: Block #{block.index}")
    print("=" * 60)
    print(f"難易度: ハッシュが '{difficulty}' で始まる必要あり")
    print(f"トランザクション数: {len(block.transactions)}\n")

    # nonceを0から順に試す
    block.nonce = 0

    while True:
        # ハッシュを計算
        computed_hash = block.compute_hash()

        # 進行状況表示（1000回ごと）
        if block.nonce % 1000 == 0:
            print(
                f"試行回数: {block.nonce:,} | 現在のハッシュ: {computed_hash[:32]}..."
            )

        # 難易度条件をチェック
        if computed_hash.startswith(difficulty):
            # 成功！
            block.hash = computed_hash
            print("\n" + "=" * 60)
            print("[OK] マイニング成功！")
            print("=" * 60)
            print(f"Nonce: {block.nonce:,}")
            print(f"Hash: {block.hash}")
            print(f"試行回数: {block.nonce + 1:,}")
            print("=" * 60 + "\n")
            return block

        # 次のnonceを試す
        block.nonce += 1

        # 安全装置（無限ループ防止）
        if block.nonce > 10_000_000:
            print("[!] 警告: 試行回数が1000万を超えました")
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
    print("\n" + "=" * 60)
    print(" ジェネシスブロック作成")
    print("=" * 60)

    genesis = Block(
        index=0,
        transactions=[{"from": "SYSTEM", "to": "NETWORK", "amount": 0, "timestamp": 0}],
        previous_hash="0" * 64,  # 64文字の0
    )

    # ジェネシスブロックは難易度低めでマイニング
    genesis = mine(genesis, difficulty="0")

    print("[OK] ジェネシスブロック作成完了")
    print("=" * 60 + "\n")

    return genesis


if __name__ == "__main__":
    print("=== マイナーモジュール テスト ===\n")

    # ジェネシスブロック作成
    genesis = create_genesis_block()
    print(f"ジェネシスブロック: {genesis}\n")

    # 通常ブロックのマイニング
    transactions = [
        {"from": "Alice", "to": "Bob", "amount": 50, "timestamp": 1234567890},
        {"from": "Bob", "to": "Carol", "amount": 30, "timestamp": 1234567891},
    ]

    block = Block(index=1, transactions=transactions, previous_hash=genesis.hash)

    # 難易度 "00" でマイニング
    mined_block = mine(block, difficulty="00")
    print(f"\nマイニング結果:\n{mined_block}")
