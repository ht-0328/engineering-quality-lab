"""会議室予約（架空の題材）のテストコード。

テスト仕様書のどの項目かを、テスト名の ID（UT-01 など）で示す。
"""

import unittest
from datetime import datetime

from reservation import (
    InMemoryReservationRepository,
    InvalidPeriod,
    ReservationConflict,
    ReservationService,
    overlaps,
)


def at(hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 12, 1, hour, minute)


class OverlapsTest(unittest.TestCase):
    """単体テスト。入力は詳細設計 DD-01。"""

    def test_ut01_partly_overlapping_periods_overlap(self) -> None:
        self.assertTrue(overlaps(at(10), at(11), at(10, 30), at(11, 30)))

    def test_ut02_touching_periods_do_not_overlap(self) -> None:
        self.assertFalse(overlaps(at(10), at(11), at(11), at(12)))
        self.assertFalse(overlaps(at(11), at(12), at(10), at(11)))

    def test_ut03_period_inside_another_overlaps(self) -> None:
        self.assertTrue(overlaps(at(10), at(12), at(10, 30), at(11)))

    def test_ut04_separate_periods_do_not_overlap(self) -> None:
        self.assertFalse(overlaps(at(10), at(11), at(13), at(14)))


class ReservationServiceTest(unittest.TestCase):
    """結合テスト（処理と保存先をつないで確かめる）。入力は詳細設計 DD-02。"""

    def setUp(self) -> None:
        self.repository = InMemoryReservationRepository()
        self.service = ReservationService(self.repository)
        self.service.reserve("room-A", at(10), at(11), "user-1")

    def test_it01_overlapping_reservation_is_rejected_and_not_saved(self) -> None:
        with self.assertRaises(ReservationConflict):
            self.service.reserve("room-A", at(10, 30), at(11, 30), "user-2")
        self.assertEqual(len(self.repository.find_by_room("room-A")), 1)

    def test_it02_same_period_in_another_room_is_accepted(self) -> None:
        self.service.reserve("room-B", at(10), at(11), "user-2")
        self.assertEqual(len(self.repository.find_by_room("room-B")), 1)

    def test_it03_following_period_in_same_room_is_accepted(self) -> None:
        self.service.reserve("room-A", at(11), at(12), "user-2")
        self.assertEqual(len(self.repository.find_by_room("room-A")), 2)

    def test_it04_end_not_after_start_is_rejected(self) -> None:
        with self.assertRaises(InvalidPeriod):
            self.service.reserve("room-A", at(13), at(13), "user-2")


if __name__ == "__main__":
    unittest.main()
