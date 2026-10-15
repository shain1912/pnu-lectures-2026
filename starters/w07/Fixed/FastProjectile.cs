// ============================================================
// 7주차 · AI 함정 #6 정답본 ③ — 빠른 물체의 연속 충돌 판정(CCD) 설정
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 터널링 조건 : 속도 × Fixed Timestep  >  (가장 얇은 벽 두께 + 물체 크기)
//   예) 40 m/s × 0.02 s = 0.8 m  >  0.2 m + 0.25 m  → 이산 판정이면 벽을 건너뛸 수 있음
//
// 모드 선택
//   Discrete              : 도착 자리만 검사 (기본값 · 가장 쌈)
//   Continuous            : 정적 Collider(벽·바닥)에 대해 경로 검사
//   ContinuousDynamic     : 정적 + 다른 Continuous 계열 물체까지 경로 검사 (가장 비쌈)
//   ContinuousSpeculative : 다가오는 접촉을 미리 예측 · Kinematic 에도 동작 (유령 충돌 가능)
//
// 사용법 : 작은 Sphere 에 Rigidbody + 이 스크립트 → 시작하면 forward 방향으로 발사
// ============================================================
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class FastProjectile : MonoBehaviour
{
    public float speed = 40f;
    public float thinnestWall = 0.2f;   // 씬에서 가장 얇은 벽 두께 (m)
    public bool autoChooseMode = true;  // 부등식으로 모드 자동 결정

    void Start()
    {
        var rb = GetComponent<Rigidbody>();
        rb.useGravity = false;

        if (autoChooseMode)
        {
            float size = GetComponent<Collider>().bounds.size.magnitude * 0.577f; // 대략적 지름
            float step = speed * Time.fixedDeltaTime;
            bool risky = step > thinnestWall + size;
            rb.collisionDetectionMode = risky
                ? CollisionDetectionMode.ContinuousDynamic
                : CollisionDetectionMode.Discrete;
            Debug.Log($"[FastProjectile] 한 스텝 {step:F2} m vs 벽+크기 {thinnestWall + size:F2} m → {rb.collisionDetectionMode}");
        }

        // 위치가 아니라 속도를 줌 → 이후 이동·충돌은 물리 엔진이 계산
        rb.AddForce(transform.forward * speed, ForceMode.VelocityChange);
    }
}
