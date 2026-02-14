"""
ブロックチェーン管理モジュール

ブロックチェーン全体の管理を行う。
- ブロックの読み込み・保存
- ブロックの追加
- チェーンの検証
- チェーンの表示
"""

import json
import os
import sys
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.simple_blockchain.block import Block


def load_blockchain() -> list[Block]:
    """
    保存されているすべてのブロックを読み込む

    Returns:
        list[Block]: ブロックのリスト（index順）
    """
    blocks = []
    blocks_dir = "data/blocks"

    # ディレクトリが存在しない場合
    if not os.path.exists(blocks_dir):
        return blocks

    # すべての .json ファイルを読み込み
    filenames = [f for f in os.listdir(blocks_dir) if f.endswith(".json")]

    for filename in sorted(filenames):
        filepath = os.path.join(blocks_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            block_data = json.load(f)
            block = Block.from_dict(block_data)
            blocks.append(block)

    # index順にソート（念のため）
    blocks.sort(key=lambda b: b.index)

    return blocks


def get_last_block() -> Optional[Block]:
    """
    最後のブロックを取得

    Returns:
        Optional[Block]: 最後のブロック。ブロックがない場合はNone
    """
    chain = load_blockchain()

    if not chain:
        return None

    return chain[-1]


def save_block(block: Block):
    """
    ブロックをファイルに保存

    Args:
        block: 保存するブロック
    """
    os.makedirs("data/blocks", exist_ok=True)

    # ファイル名: block-0001.json 形式
    filename = f"data/blocks/block-{block.index:04d}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(block.to_dict(), f, indent=2, ensure_ascii=False)

    print(f"[OK] ブロック保存完了: {filename}")


def add_block(block: Block) -> bool:
    """
    新しいブロックをチェーンに追加

    Args:
        block: 追加するブロック

    Returns:
        bool: 追加に成功したらTrue
    """
    # 最後のブロックを取得
    last_block = get_last_block()

    if last_block is None:
        # ジェネシスブロックの場合
        if block.index != 0:
            print("[NG] エラー: 最初のブロックはindex=0である必要があります")
            return False
    else:
        # 通常ブロックの場合
        expected_index = last_block.index + 1

        if block.index != expected_index:
            print(
                f"[NG] エラー: ブロックindexが不正です（期待値: {expected_index}、実際: {block.index}）"
            )
            return False

        if block.previous_hash != last_block.hash:
            print("[NG] エラー: previous_hashが前のブロックと一致しません")
            return False

    # ブロックを保存
    save_block(block)
    return True


def verify_chain() -> bool:
    """
    ブロックチェーン全体の整合性を検証

    Returns:
        bool: チェーンが有効ならTrue
    """
    print("\n" + "=" * 60)
    print(" ブロックチェーン検証")
    print("=" * 60)

    chain = load_blockchain()

    if not chain:
        print("[!] 警告: ブロックが1つもありません")
        print("=" * 60 + "\n")
        return True

    print(f"検証対象: {len(chain)} ブロック\n")

    # 各ブロックを検証
    for i, block in enumerate(chain):
        print(f"Block #{block.index} を検証中...")

        # 1. ハッシュの再計算
        computed_hash = block.compute_hash()
        if computed_hash != block.hash:
            print(f"[NG] エラー: Block #{block.index} のハッシュが不正です")
            print(f"   保存されたハッシュ: {block.hash}")
            print(f"   再計算されたハッシュ: {computed_hash}")
            print("   → ブロックが改ざんされた可能性があります")
            print("=" * 60 + "\n")
            return False

        # 2. previous_hash の検証（ジェネシスブロック以外）
        if i > 0:
            previous_block = chain[i - 1]
            if block.previous_hash != previous_block.hash:
                print(f"[NG] エラー: Block #{block.index} のprevious_hashが不正です")
                print(f"   期待値: {previous_block.hash}")
                print(f"   実際の値: {block.previous_hash}")
                print("   → チェーンの連鎖が破壊されています")
                print("=" * 60 + "\n")
                return False

        print(f"   [OK] Block #{block.index} は正常です")

    print("\n" + "=" * 60)
    print("[OK] ブロックチェーン検証成功！")
    print("   すべてのブロックが整合性を保っています")
    print("=" * 60 + "\n")

    return True


def display_chain():
    """
    ブロックチェーン全体を表示
    """
    print("\n" + "=" * 60)
    print(" ブロックチェーン")
    print("=" * 60)

    chain = load_blockchain()

    if not chain:
        print("ブロックがまだありません")
        print("まずはジェネシスブロックを作成してください")
    else:
        print(f"総ブロック数: {len(chain)}\n")

        for block in chain:
            print("-" * 60)
            print(f"Block #{block.index}")
            print(f"  タイムスタンプ: {block.timestamp}")
            print(f"  トランザクション数: {len(block.transactions)}")

            # トランザクション詳細
            for i, tx in enumerate(block.transactions, 1):
                print(f"    {i}. {tx['from']} → {tx['to']}: {tx['amount']}")

            print(f"  Previous Hash: {block.previous_hash[:16]}...")
            print(f"  Nonce: {block.nonce}")
            print(f"  Hash: {block.hash[:16]}...")

    print("=" * 60 + "\n")


def get_chain_status() -> dict:
    """
    チェーンの現在の状態を取得

    Returns:
        dict: チェーンの状態情報
    """
    chain = load_blockchain()

    return {
        "block_count": len(chain),
        "last_block_index": chain[-1].index if chain else -1,
        "last_block_hash": chain[-1].hash if chain else None,
    }


if __name__ == "__main__":
    sys.path.insert(0, "src")

    from simple_blockchain.miner import mine, create_genesis_block

    print("=== ブロックチェーン管理モジュール テスト ===\n")

    # ジェネシスブロック作成
    print("1. ジェネシスブロック作成")
    genesis = create_genesis_block()
    add_block(genesis)

    # チェーン表示
    print("\n2. チェーン表示")
    display_chain()

    # ブロック追加
    print("\n3. 新しいブロック追加")
    transactions = [
        {"from": "Alice", "to": "Bob", "amount": 100, "timestamp": 1234567890}
    ]

    block1 = Block(index=1, transactions=transactions, previous_hash=genesis.hash)

    mined_block1 = mine(block1, difficulty="0")
    add_block(mined_block1)

    # チェーン表示
    print("\n4. チェーン表示")
    display_chain()

    # チェーン検証
    print("\n5. チェーン検証")
    verify_chain()

    # 状態取得
    print("\n6. チェーン状態")
    status = get_chain_status()
    print(f"ブロック数: {status['block_count']}")
    print(f"最後のブロック: #{status['last_block_index']}")
