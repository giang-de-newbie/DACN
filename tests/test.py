# -*- coding: utf-8 -*-
import sys
import os
from nlp.nlp_engine import NLPEngine
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

TEST_CASES = [
    {'input': 'Nhac toi hop nhom luc 10 gio sang mai o phong 302', 'expected': {'event': 'hop nhom', 'location': 'phong 302', 'reminder_minutes': 15}},
    {'input': 'Can nen gap toi vao 9 gio hom nay', 'expected': {'event': 'gap', 'reminder_minutes': 15}},
    {'input': 'Hoi hop team meeting vao luc 14 gio 30 tai van phong', 'expected': {'event': 'hoi hop', 'location': 'van phong', 'reminder_minutes': 15}},
    {'input': 'Nhac toi di hoc luc 7 gio sang', 'expected': {'event': 'di hoc', 'reminder_minutes': 15}},
    {'input': 'Sinh nhat ban be mai vao 18 gio tai nha hang', 'expected': {'event': 'sinh nhat', 'location': 'nha hang', 'reminder_minutes': 15}},
    {'input': 'Phong van tai cong ty A vao 10 gio sang ngay 25/11', 'expected': {'event': 'phong van', 'location': 'cong ty A', 'reminder_minutes': 15}},
    {'input': 'Deadline nop bai tap luc 23 gio 59', 'expected': {'event': 'deadline', 'reminder_minutes': 15}},
    {'input': 'Thi kiem tra mon toan vao 9 gio sang mai', 'expected': {'event': 'thi', 'reminder_minutes': 15}},
    {'input': 'Goi dien cho boss vao 3 gio chieu', 'expected': {'event': 'goi dien', 'reminder_minutes': 15}},
    {'input': 'Meeting review duan vao 2 gio chieu tai phong A101', 'expected': {'event': 'meeting', 'location': 'phong A101', 'reminder_minutes': 15}},
    {'input': 'Du seminar ve AI vao sang 25/11 gio 9', 'expected': {'event': 'du seminar', 'reminder_minutes': 15}},
    {'input': 'Lam bai tap luc 6 gio toi hom nay', 'expected': {'event': 'lam bai tap', 'reminder_minutes': 15}},
    {'input': 'Hen gap ban ho vao chieu 3 gio o cafe', 'expected': {'event': 'hen gap', 'location': 'cafe', 'reminder_minutes': 15}},
    {'input': 'Tham du hoi nghi toan quoc vao 10 gio sang thu hai toi', 'expected': {'event': 'tham du', 'reminder_minutes': 15}},
    {'input': 'Nhan nham khong can vao luc nao', 'expected': {}},
    {'input': 'hop', 'expected': {'event': 'hop', 'reminder_minutes': 15}},
    {'input': 'Kiem tra suc khoe vao 8 gio sang', 'expected': {'event': 'kiem tra', 'reminder_minutes': 15}},
    {'input': 'Du lich den nhat ban vao 7h sang 1/12', 'expected': {'event': 'du lich', 'reminder_minutes': 15}},
    {'input': 'Tap luyen co the luc 17 gio chieu hom qua', 'expected': {'event': 'tap luyen', 'reminder_minutes': 15}},
    {'input': 'Tuan hop team vao 10h30 sang ok', 'expected': {'event': 'tuan hop', 'reminder_minutes': 15}},
    {'input': 'Thao luan voi nhom luc 19h toi mai', 'expected': {'event': 'thao luan', 'reminder_minutes': 15}},
    {'input': 'Nham toi nhac khi ok den 9 gio sang', 'expected': {'event': 'nhac', 'reminder_minutes': 15}},
    {'input': 'Dam me gap mme o nha hang tai sai gon 12h trua mai', 'expected': {'event': 'dam me gap', 'location': 'sai gon', 'reminder_minutes': 15}},
    {'input': 'Hoc lam ban tu 8h den 11h30 sang mai', 'expected': {'event': 'hoc lam ban', 'reminder_minutes': 15}},
    {'input': 'Chay bo o cong vien luc 6h sang hom nay', 'expected': {'event': 'chay bo', 'location': 'cong vien', 'reminder_minutes': 15}},
    {'input': 'Di mua sop o sieu thi luc 9h sang', 'expected': {'event': 'di mua', 'location': 'sieu thi', 'reminder_minutes': 15}},
    {'input': 'hop hop hop', 'expected': {'event': 'hop hop hop', 'reminder_minutes': 15}},
    {'input': 'Xem phim vao 19h30 toi mai tai rap chieu phim', 'expected': {'event': 'xem phim', 'location': 'rap chieu phim', 'reminder_minutes': 15}},
    {'input': 'Nhai nham khong khong', 'expected': {'event': 'nhai nham', 'reminder_minutes': 15}},
    {'input': 'Tong ket nam hoc vao 9 gio sang thu 4 tai hoi truong', 'expected': {'event': 'tong ket', 'location': 'hoi truong', 'reminder_minutes': 15}},
]

def check_field(result, expected, field):
    if field not in expected:
        return True
    if expected[field] is None:
        return result.get(field) is None
    if field in ['event', 'location']:
        expected_val = str(expected[field]).lower()
        result_val = str(result.get(field, '')).lower()
        return expected_val in result_val or result_val in expected_val
    if field == 'reminder_minutes':
        return result.get('reminder_minutes') == expected[field]
    return True

def run_tests():
    print('=' * 60)
    print('KIEM TRA DO CHINH XAC NLP ENGINE')
    print('=' * 60)
    print(f'Tong so test cases: {len(TEST_CASES)}\n')

    engine = NLPEngine()
    total_tests = len(TEST_CASES)
    passed_tests = 0
    failed_cases = []

    for i, test_case in enumerate(TEST_CASES, 1):
        input_text = test_case['input']
        expected = test_case['expected']

        print(f'[Test {i}/{total_tests}] {input_text[:50]}...')

        try:
            result = engine.extract(input_text)
            all_passed = True
            for field, expected_value in expected.items():
                passed = check_field(result, expected, field)
                if not passed:
                    all_passed = False
                    print(f'  FAIL - {field}: expected {expected_value}, got {result.get(field)}')

            if all_passed and expected:
                print('  PASS')
                passed_tests += 1
            elif not expected and not result.get('event'):
                print('  PASS (empty expected)')
                passed_tests += 1
            else:
                failed_cases.append({'input': input_text, 'expected': expected, 'result': result})
        except Exception as e:
            print(f'  ERROR: {str(e)}')
            failed_cases.append({'input': input_text, 'error': str(e)})

    print('\n' + '=' * 60)
    print('TONG KET:')
    print(f'Tong tests: {total_tests}')
    print(f'Passed: {passed_tests}')
    print(f'Failed: {total_tests - passed_tests}')
    accuracy = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f'Accuracy: {accuracy:.2f}%')
    print('=' * 60)

    if accuracy >= 80:
        print('KET QUA: DAT YEU CAU (>= 80%)')
    else:
        print('KET QUA: CHUA DAT YEU CAU (< 80%)')
        print('\nFailing cases (first 5):')
        for i, case in enumerate(failed_cases[:5], 1):
            print(f'{i}. Input: {case["input"][:60]}')
            if 'error' in case:
                print(f'   Error: {case["error"]}')
            else:
                print(f'   Expected: {case.get("expected", {})}')
                print(f'   Result: {case.get("result", {})}')

if __name__ == '__main__':
    run_tests()
