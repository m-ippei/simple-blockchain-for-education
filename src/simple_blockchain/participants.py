"""
参加者管理モジュール

ブロックチェーンに参加するユーザー（アドレス）の管理を行う。
- participants.json から参加者データを読み込み
- アドレスの有効性を検証
"""

import json
import os


def load_participants() -> list[str]:
    """
    参加者リストをJSONファイルから読み込む

    Returns:
        list[str]: 参加者名のリスト

    Raises:
        FileNotFoundError: participants.jsonが存在しない場合
    """
    filepath = "data/participants.json"

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} が見つかりません")

    with open(filepath, "r", encoding="utf-8") as f:
        participants = json.load(f)

    return participants


def is_valid_address(address: str) -> bool:
    """
    アドレスが有効かどうかを判定する

    検証項目:
    1. 長さが3〜5文字であること
    2. participants.jsonに登録済みであること

    Args:
        address: 検証するアドレス

    Returns:
        bool: 有効なら True
    """
    # 長さチェック
    if not (3 <= len(address) <= 5):
        return False

    # 登録済みかチェック
    participants = load_participants()
    return address in participants


def display_participants():
    """
    参加者一覧を表示する
    """
    print("\n" + "=" * 40)
    print(" 登録済み参加者一覧")
    print("=" * 40)

    participants = load_participants()
    for i, name in enumerate(participants, 1):
        print(f"{i}. {name}")

    print("=" * 40 + "\n")


if __name__ == "__main__":
    print("=== 参加者管理モジュール テスト ===\n")

    # 参加者一覧表示
    display_participants()

    # アドレス検証テスト
    test_addresses = ["Alice", "Bob", "Unknown", "X"]
    for addr in test_addresses:
        result = is_valid_address(addr)
        print(f"{addr}: {'[OK] 有効' if result else '[NG] 無効'}")
