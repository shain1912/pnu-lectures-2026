// ============================================================
// 7주차 · 측정 도구 — 벽 통과(터널링) 횟수 세기
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 하는 일 : 같은 속도로 공 count 개를 얇은 벽에 발사 → 일정 시간 뒤 벽 뒤에 있는 공 수 로그
//   - 시작 위치를 한 스텝 이동 거리 안에서 무작위로 흩뜨림 → 터널링은 "확률적" 이므로 여러 번 시험
//   - 검증 조건 예 : "대시 속도 40 m/s 로 20회 발사 → 통과 0회"
//
// 모드
//   TransformPosition   : Rigidbody 가 붙은 공을 transform.position 으로 이동 (함정 재현)
//   RigidbodyDiscrete   : linearVelocity 로 이동 · Collision Detection = Discrete
//   RigidbodyContinuous : linearVelocity 로 이동 · Collision Detection = Continuous Dynamic
//
// 사용법
//   1) Cube 하나를 벽으로 : Scale (6, 3, 0.2) → 두께 = z 축 0.2 m · BoxCollider 유지
//   2) 빈 GameObject 에 이 스크립트 → wall 에 그 Cube 지정
//   3) 모드·속도를 바꿔 가며 Play → Console 로그를 워크북 표에 기록
//   공은 벽의 앞쪽(-forward) 5 m 지점에서 벽의 forward 방향으로 날아감
// ============================================================
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WallPassTest : MonoBehaviour
{
    public enum Mode { TransformPosition, RigidbodyDiscrete, RigidbodyContinuous }

    public Mode mode = Mode.TransformPosition;
    public Transform wall;
    public float speed = 40f;       // m/s
    public int count = 20;          // 발사 횟수
    public float ballSize = 0.25f;  // 공 지름 (m)
    public float spacing = 0.6f;    // 공 사이 가로 간격 (서로 부딪히지 않게)
    public bool runOnStart = true;

    readonly List<Rigidbody> balls = new List<Rigidbody>();
    Vector3 fwd;

    void Start()
    {
        if (runOnStart) StartCoroutine(Run());
    }

    public IEnumerator Run()
    {
        if (wall == null) { Debug.LogError("[WallPassTest] wall 을 지정하세요"); yield break; }

        fwd = wall.forward;
        float halfThickness = wall.lossyScale.z * 0.5f;
        float step = speed * Time.fixedDeltaTime;

        for (int i = 0; i < count; i++)
        {
            var go = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            go.name = "WallPassBall_" + i;
            go.transform.localScale = Vector3.one * ballSize;

            float lateral = (i - (count - 1) * 0.5f) * spacing;
            float phase = Random.Range(0f, step);                       // 시작 위상 무작위
            go.transform.position = wall.position - fwd * (5f + phase) + wall.right * lateral;

            var rb = go.AddComponent<Rigidbody>();
            rb.useGravity = false;
            rb.collisionDetectionMode = mode == Mode.RigidbodyContinuous
                ? CollisionDetectionMode.ContinuousDynamic
                : CollisionDetectionMode.Discrete;
            if (mode != Mode.TransformPosition)
                rb.linearVelocity = fwd * speed;                        // 정답 : 속도로 이동
            balls.Add(rb);
        }

        yield return new WaitForSeconds(10f / speed + 0.5f);

        int passed = 0;
        foreach (var rb in balls)
            if (rb != null && Vector3.Dot(rb.position - wall.position, fwd) > halfThickness + ballSize * 0.5f)
                passed++;

        Debug.Log($"[WallPassTest] {mode} · {speed} m/s · 한 스텝 {step:F2} m · 벽 {halfThickness * 2f:F2} m · " +
                  $"{count}회 중 통과 {passed}회 ({100f * passed / count:F0}%)");

        foreach (var rb in balls) if (rb != null) Destroy(rb.gameObject);
        balls.Clear();
    }

    void Update()
    {
        if (mode != Mode.TransformPosition) return;
        // 함정 재현 : Rigidbody 가 붙은 공을 Update 에서 순간이동
        foreach (var rb in balls)
            if (rb != null) rb.transform.position += fwd * speed * Time.deltaTime;
    }
}
