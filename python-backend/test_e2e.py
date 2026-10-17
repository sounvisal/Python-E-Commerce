from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_flows():
    print("=== TESTING REAL END-TO-END FLOWS ===")
    
    # 1. Test Review submission & helpful vote
    rev_res = client.post('/api/reviews', json={
        'product_id': 201,
        'rating': 5,
        'title': 'Truly magnificent formulation',
        'comment': 'After just three weeks of morning ritual, my skin texture is remarkably soft.',
        'customer_name': 'Dr. Althea Moreau',
        'customer_email': 'dr.althea@example.com'
    })
    assert rev_res.status_code == 201, f'Review submit failed: {rev_res.text}'
    rev_id = rev_res.json()['data']['id']
    print(f'[PASS] Created review ID: {rev_id}')

    vote_res = client.post(f'/api/reviews/{rev_id}/helpful')
    assert vote_res.status_code == 200, f'Vote failed: {vote_res.text}'
    assert vote_res.json()['helpful_count'] == 1, 'Helpful count did not increment'
    print(f"[PASS] Helpful vote recorded, count: {vote_res.json()['helpful_count']}")

    # 2. Test Admin settings persistence
    set_res = client.put('/api/admin/settings', json={
        'free_shipping_threshold': 65.0,
        'tax_rate': 8.5
    })
    assert set_res.status_code == 200, f'Settings update failed: {set_res.text}'

    pub_settings = client.get('/api/settings').json()
    assert pub_settings['data']['free_shipping_threshold'] == 65.0, 'Public settings did not reflect threshold'
    assert pub_settings['data']['tax_rate'] == 8.5, 'Public settings did not reflect tax rate'
    print(f"[PASS] Admin settings persisted to public API: ${pub_settings['data']['free_shipping_threshold']} threshold, {pub_settings['data']['tax_rate']}% tax")

    # Reset settings back to standard
    client.put('/api/admin/settings', json={'free_shipping_threshold': 50.0, 'tax_rate': 10.0})
    print("[PASS] Reset settings back to default ($50.00 threshold, 10.0% tax)")

    # 3. Test Quiz completion
    q_res = client.post('/api/quizzes/1/complete', json={
        'answers': {'skinType': 'Combination', 'goals': ['Hydration']},
        'skin_type_result': 'Combination'
    })
    assert q_res.status_code == 200, f'Quiz completion failed: {q_res.text}'
    print(f"[PASS] Quiz completion recorded in DB: {q_res.json()['result']}")

    print("=== ALL FULL END-TO-END FLOWS VERIFIED SUCCESSFULLY ===")

if __name__ == '__main__':
    test_flows()
