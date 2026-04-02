"""
Autograder for the List/Tuple assignment.

Usage in Colab or Python:

import autograder as ag

# After defining the student's functions in the notebook:
results = ag.run_all(globals())
ag.print_report(results)

# Optional:
score = ag.total_score(results)
print(score)
"""

from typing import Any, Callable, Dict, List, Tuple
import math

EXPECTED_FUNCTIONS = [
    "step1_count_students",
    "step2_get_names",
    "step3_find_name_by_id",
    "step4_average_scores",
    "step5_students_with_average_at_least_80",
    "step6_add_student",
    "step7_add_score_to_student",
    "step8_top_student",
    "step9_merge_student_data",
    "step10_sort_by_average_desc",
]


def get_base_data():
    students = [
        (1, "Alice"),
        (2, "Bob"),
        (3, "Charlie"),
    ]
    scores = [
        [80, 90],
        [70, 85],
        [100, 95],
    ]
    return students, scores


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float))


def _deepcopy_students_scores():
    students, scores = get_base_data()
    students_copy = [(sid, name) for sid, name in students]
    scores_copy = [row[:] for row in scores]
    return students_copy, scores_copy


def _call(func: Callable, *args, **kwargs):
    try:
        return True, func(*args, **kwargs), None
    except Exception as e:
        return False, None, f"{type(e).__name__}: {e}"


def _normalize_name_list(x):
    if isinstance(x, tuple):
        x = list(x)
    return x


def _almost_equal(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol


def test_step1(func: Callable):
    students, _ = get_base_data()
    ok, result, err = _call(func, students)
    if not ok:
        return False, f"실행 중 오류: {err}"
    if result == 3:
        return True, "통과"
    return False, f"기대값 3, 실제값 {result}"


def test_step2(func: Callable):
    students, _ = get_base_data()
    ok, result, err = _call(func, students)
    if not ok:
        return False, f"실행 중 오류: {err}"
    result = _normalize_name_list(result)
    expected = ["Alice", "Bob", "Charlie"]
    if result == expected:
        return True, "통과"
    return False, f"기대값 {expected}, 실제값 {result}"


def test_step3(func: Callable):
    students, _ = get_base_data()
    ok, result, err = _call(func, students, 2)
    if not ok:
        return False, f"실행 중 오류: {err}"
    if result == "Bob":
        return True, "통과"
    return False, f"기대값 'Bob', 실제값 {result}"


def test_step4(func: Callable):
    _, scores = get_base_data()
    ok, result, err = _call(func, scores)
    if not ok:
        return False, f"실행 중 오류: {err}"
    expected = [85.0, 77.5, 97.5]
    if not isinstance(result, (list, tuple)) or len(result) != len(expected):
        return False, f"길이 {len(expected)}의 리스트/튜플을 반환해야 합니다. 실제값: {result}"
    for a, b in zip(result, expected):
        if not _is_number(a) or not _almost_equal(float(a), float(b)):
            return False, f"기대값 {expected}, 실제값 {result}"
    return True, "통과"


def test_step5(func: Callable):
    students, scores = get_base_data()
    ok, result, err = _call(func, students, scores)
    if not ok:
        return False, f"실행 중 오류: {err}"
    result = _normalize_name_list(result)
    expected = ["Alice", "Charlie"]
    if result == expected:
        return True, "통과"
    return False, f"기대값 {expected}, 실제값 {result}"


def test_step6(func: Callable):
    students, scores = _deepcopy_students_scores()
    ok, result, err = _call(func, students, scores, (4, "David"), [60, 70])
    if not ok:
        return False, f"실행 중 오류: {err}"

    # 허용 방식:
    # 1) students, scores를 직접 수정하고 None 반환
    # 2) (new_students, new_scores) 반환
    if result is None:
        new_students, new_scores = students, scores
    elif isinstance(result, tuple) and len(result) == 2:
        new_students, new_scores = result
    else:
        return False, "None 또는 (students, scores) 형태를 반환해야 합니다."

    expected_students = [
        (1, "Alice"),
        (2, "Bob"),
        (3, "Charlie"),
        (4, "David"),
    ]
    expected_scores = [
        [80, 90],
        [70, 85],
        [100, 95],
        [60, 70],
    ]

    if new_students == expected_students and new_scores == expected_scores:
        return True, "통과"
    return False, f"기대 students={expected_students}, scores={expected_scores}, 실제 students={new_students}, scores={new_scores}"


def test_step7(func: Callable):
    students, scores = _deepcopy_students_scores()
    ok, result, err = _call(func, students, scores, "Alice", 100)
    if not ok:
        return False, f"실행 중 오류: {err}"

    if result is None:
        new_scores = scores
    else:
        new_scores = result

    expected_scores = [
        [80, 90, 100],
        [70, 85],
        [100, 95],
    ]
    if new_scores == expected_scores:
        return True, "통과"
    return False, f"기대값 {expected_scores}, 실제값 {new_scores}"


def test_step8(func: Callable):
    students, scores = get_base_data()
    ok, result, err = _call(func, students, scores)
    if not ok:
        return False, f"실행 중 오류: {err}"
    if result == "Charlie":
        return True, "통과"
    return False, f"기대값 'Charlie', 실제값 {result}"


def test_step9(func: Callable):
    students = [
        (1, "Alice"),
        (2, "Bob"),
        (3, "Charlie"),
    ]
    scores = [
        [80, 90, 100],
        [70, 85],
        [100, 95],
    ]
    ok, result, err = _call(func, students, scores)
    if not ok:
        return False, f"실행 중 오류: {err}"
    expected = [
        (1, "Alice", [80, 90, 100]),
        (2, "Bob", [70, 85]),
        (3, "Charlie", [100, 95]),
    ]
    if result == expected:
        return True, "통과"
    return False, f"기대값 {expected}, 실제값 {result}"


def test_step10(func: Callable):
    merged = [
        (1, "Alice", [80, 90, 100]),   # avg 90
        (2, "Bob", [70, 85]),          # avg 77.5
        (3, "Charlie", [100, 95]),     # avg 97.5
    ]
    ok, result, err = _call(func, merged)
    if not ok:
        return False, f"실행 중 오류: {err}"
    expected = [
        (3, "Charlie", [100, 95]),
        (1, "Alice", [80, 90, 100]),
        (2, "Bob", [70, 85]),
    ]
    if result == expected:
        return True, "통과"
    return False, f"기대값 {expected}, 실제값 {result}"


TESTS = {
    "step1_count_students": test_step1,
    "step2_get_names": test_step2,
    "step3_find_name_by_id": test_step3,
    "step4_average_scores": test_step4,
    "step5_students_with_average_at_least_80": test_step5,
    "step6_add_student": test_step6,
    "step7_add_score_to_student": test_step7,
    "step8_top_student": test_step8,
    "step9_merge_student_data": test_step9,
    "step10_sort_by_average_desc": test_step10,
}


def run_all(namespace: Dict[str, Any]) -> List[Dict[str, Any]]:
    results = []
    for name in EXPECTED_FUNCTIONS:
        if name not in namespace:
            results.append({
                "function": name,
                "passed": False,
                "message": "함수가 정의되어 있지 않습니다."
            })
            continue

        func = namespace[name]
        passed, message = TESTS[name](func)
        results.append({
            "function": name,
            "passed": passed,
            "message": message
        })
    return results


def total_score(results: List[Dict[str, Any]]) -> str:
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    return f"{passed}/{total}"


def print_report(results: List[Dict[str, Any]]) -> None:
    print("=" * 60)
    print("자동 채점 결과")
    print("=" * 60)
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"[{status}] {r['function']}")
        print(f"  - {r['message']}")
    print("-" * 60)
    print(f"총점: {total_score(results)}")
    print("=" * 60)
