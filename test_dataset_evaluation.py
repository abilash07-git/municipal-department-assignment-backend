import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ai_conflict_engine import AIConflictEngine

def run_evaluation():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset_multi_department_conflicts.json")
    with open(data_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    correct = 0
    total = len(dataset)

    print("=" * 80)
    print(f"EVALUATING AI MULTI-DEPARTMENT CONFLICT ENGINE ON {total} BENCHMARK CASES")
    print("=" * 80)

    for case in dataset:
        res = AIConflictEngine.analyze_conflict(
            hazard_type=case["hazard_type"],
            description=case["description"],
            ward=case["ward"],
            is_ward_boundary=case["is_ward_boundary"]
        )
        gt = case["ground_truth"]

        conflict_match = (res["is_conflict_detected"] == gt["is_conflict_detected"])
        primary_match = (res["primary_department"]["id"] == gt["primary_department_id"])
        sec_gt = gt["secondary_department_id"]
        sec_pred = res["secondary_department"]["id"] if res["secondary_department"] else None
        sec_match = (sec_pred == sec_gt)
        rule_match = (res["ownership_rule_applied"] == gt["ownership_rule_applied"])

        is_success = (conflict_match and primary_match and sec_match and rule_match)
        if is_success:
            correct += 1
            print(f"[{case['id']}] PASS: {res['conflict_type']}")
            print(f"         Primary: {res['primary_department']['code']} | Secondary: {sec_pred} | Rule: {res['ownership_rule_applied']}")
        else:
            print(f"[{case['id']}] FAIL:")
            print(f"  Predicted: conflict={res['is_conflict_detected']}, primary={res['primary_department']['id']}, sec={sec_pred}, rule={res['ownership_rule_applied']}")
            print(f"  GroundTr:  conflict={gt['is_conflict_detected']}, primary={gt['primary_department_id']}, sec={sec_gt}, rule={gt['ownership_rule_applied']}")

    accuracy = (correct / total) * 100
    print("=" * 80)
    print(f"BENCHMARK ACCURACY: {accuracy:.1f}% ({correct}/{total} passed)")
    print("=" * 80)
    assert accuracy == 100.0, f"Expected 100% accuracy, got {accuracy}%"

if __name__ == "__main__":
    run_evaluation()
