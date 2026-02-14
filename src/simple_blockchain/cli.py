"""
CLIアプリケーションモジュール

学習用ブロックチェーンの対話的CLIアプリケーション。
すべての機能を統合して提供する。
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.simple_blockchain import participants, transaction, blockchain, miner
from src.simple_blockchain.block import Block


def display_header():
    """
    CLIのヘッダーを表示
    """
    print("\n" + "=" * 60)
    print(" Simple Blockchain - 学習用ブロックチェーン")
    print("=" * 60)


def display_status():
    """
    現在の状態を表示
    """
    status = blockchain.get_chain_status()
    pending_count = len(transaction.get_pending_transactions())

    print(f"\n現在のブロック数: {status['block_count']}")
    print(f"未処理トランザクション: {pending_count}")


def display_menu():
    """
    メニューを表示
    """
    print("\n" + "-" * 60)
    print("[1] 参加者一覧")
    print("[2] トランザクション作成")
    print("[3] 未処理トランザクション表示")
    print("[4] マイニング実行")
    print("[5] チェーン表示")
    print("[6] チェーン検証")
    print("[7] ブロック改ざん（学習用）")
    print("[8] 終了")
    print("-" * 60)


def handle_menu_1():
    """
    [1] 参加者一覧
    """
    participants.display_participants()


def handle_menu_2():
    """
    [2] トランザクション作成
    """
    transaction.create_transaction()


def handle_menu_3():
    """
    [3] 未処理トランザクション表示
    """
    transaction.display_pending_transactions()


def handle_menu_4():
    """
    [4] マイニング実行
    """
    # 未処理トランザクションを取得
    pending_txs = transaction.get_pending_transactions()

    if not pending_txs:
        print("\n[!] 未処理トランザクションがありません")
        print("まずトランザクションを作成してください")
        return

    # 最後のブロックを取得
    last_block = blockchain.get_last_block()

    if last_block is None:
        # ジェネシスブロックを作成
        print("\n最初のブロック（ジェネシスブロック）を作成します...")
        genesis = miner.create_genesis_block()
        blockchain.add_block(genesis)

        # もう一度最後のブロックを取得
        last_block = blockchain.get_last_block()

    # 念のため、last_block が None でないことを確認
    if last_block is None:
        print("[NG] ブロックの取得に失敗しました")
        return

    # 新しいブロックを作成
    new_index = last_block.index + 1
    new_block = Block(
        index=new_index, transactions=pending_txs, previous_hash=last_block.hash
    )

    # マイニング実行
    mined_block = miner.mine(new_block, difficulty="00")

    # チェーンに追加
    if blockchain.add_block(mined_block):
        print("[OK] ブロックがチェーンに追加されました")

        # 未処理トランザクションをクリア
        transaction.clear_pending_transactions()
        print("[OK] 未処理トランザクションをクリアしました")
    else:
        print("[NG] ブロックの追加に失敗しました")


def handle_menu_5():
    """
    [5] チェーン表示
    """
    blockchain.display_chain()


def handle_menu_6():
    """
    [6] チェーン検証
    """
    blockchain.verify_chain()


def handle_menu_7():
    """
    [7] ブロック改ざん（学習用）

    特定のブロックのデータを改ざんして、検証機能を体験する
    """
    import json

    print("\n" + "=" * 60)
    print(" ブロック改ざん（学習用機能）")
    print("=" * 60)
    print("[!] この機能はブロックチェーンの改ざん検知を学ぶためのものです")

    # チェーンを読み込み
    chain = blockchain.load_blockchain()

    if not chain:
        print("\n[NG] ブロックがありません")
        return

    # ブロック一覧表示
    print(f"\n現在のブロック数: {len(chain)}")
    for block in chain:
        print(f"  Block #{block.index}: {len(block.transactions)} トランザクション")

    # ブロック番号を入力
    try:
        block_index = int(input("\n改ざんするブロック番号: ").strip())
    except ValueError:
        print("[NG] 無効な入力です")
        return

    # ブロックファイルを読み込み
    filename = f"data/blocks/block-{block_index:04d}.json"

    if not os.path.exists(filename):
        print(f"[NG] Block #{block_index} が見つかりません")
        return

    with open(filename, "r", encoding="utf-8") as f:
        block_data = json.load(f)

    # トランザクション表示
    print(f"\nBlock #{block_index} のトランザクション:")
    for i, tx in enumerate(block_data["transactions"]):
        print(f"  {i}. {tx['from']} → {tx['to']}: {tx['amount']}")

    # 改ざんするトランザクション選択
    try:
        tx_index = int(input("\n改ざんするトランザクション番号: ").strip())
    except ValueError:
        print("[NG] 無効な入力です")
        return

    if not (0 <= tx_index < len(block_data["transactions"])):
        print("[NG] 無効なトランザクション番号です")
        return

    # 新しい金額を入力
    try:
        new_amount = int(input("新しい金額: ").strip())
    except ValueError:
        print("[NG] 無効な入力です")
        return

    # データ改ざん
    old_amount = block_data["transactions"][tx_index]["amount"]
    block_data["transactions"][tx_index]["amount"] = new_amount

    # ファイルに保存
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(block_data, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("[OK] ブロックを改ざんしました")
    print("=" * 60)
    print(f"Block #{block_index}")
    print(f"トランザクション #{tx_index}")
    print(f"  変更前の金額: {old_amount}")
    print(f"  変更後の金額: {new_amount}")
    print("\n[!] ヒント: [6] チェーン検証 で改ざんが検出されます")
    print("=" * 60)


def main():
    """
    CLIアプリケーションのメインループ
    """
    while True:
        # ヘッダー表示
        display_header()

        # 状態表示
        display_status()

        # メニュー表示
        display_menu()

        # 入力受付
        try:
            choice = input("\n選択してください: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n終了します...")
            break

        # メニュー処理
        if choice == "1":
            handle_menu_1()
        elif choice == "2":
            handle_menu_2()
        elif choice == "3":
            handle_menu_3()
        elif choice == "4":
            handle_menu_4()
        elif choice == "5":
            handle_menu_5()
        elif choice == "6":
            handle_menu_6()
        elif choice == "7":
            handle_menu_7()
        elif choice == "8":
            print("\n終了します...")
            break
        else:
            print("\n[NG] 無効な選択です")

        # 次の操作まで一時停止
        input("\nEnterキーを押して続行...")


if __name__ == "__main__":
    main()
