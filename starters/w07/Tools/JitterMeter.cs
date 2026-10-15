// ============================================================
// 7주차 · 측정 도구 — 벽에 밀어붙이는 동안의 흔들림 폭
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 사용법 : 플레이어(공)에 붙임 → 벽에 계속 밀어붙인 상태에서 J 키 → 3초 동안 위치 최소·최대 기록
//   - 결과 = 최대 − 최소 (m) · 검증 조건 예 : "흔들림 폭 0.005 m 이하"
//   - TrapMover(함정) 와 RigidbodyMover(정답) 로 각각 측정해 워크북 표에 기록
// ============================================================
using UnityEngine;
using UnityEngine.InputSystem;

public class JitterMeter : MonoBehaviour
{
    public enum Axis { X, Y, Z }
    public Axis axis = Axis.Z;          // 벽에 수직인 축
    public float window = 3f;           // 측정 시간 (초)

    bool measuring;
    float t, min, max;

    void Update()
    {
        if (!measuring && Keyboard.current != null && Keyboard.current.jKey.wasPressedThisFrame)
        {
            measuring = true; t = 0f; min = float.MaxValue; max = float.MinValue;
            Debug.Log("[JitterMeter] 측정 시작 — 벽에 계속 밀어붙이세요");
        }
    }

    // 물리가 실제로 정한 위치를 보기 위해 FixedUpdate 에서 기록
    void FixedUpdate()
    {
        if (!measuring) return;
        Vector3 p = transform.position;
        float v = axis == Axis.X ? p.x : axis == Axis.Y ? p.y : p.z;
        min = Mathf.Min(min, v); max = Mathf.Max(max, v);
        t += Time.fixedDeltaTime;
        if (t >= window)
        {
            measuring = false;
            Debug.Log($"[JitterMeter] {window:F0}초 동안 {axis} 축 흔들림 폭 {(max - min):F4} m");
        }
    }
}
