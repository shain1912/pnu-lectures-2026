// ============================================================
// 7주차 · AI 함정 #6 정답본 ② — Is Kinematic 물체를 MovePosition 으로 움직이기
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 용도 : 엘리베이터 · 자동문 · 움직이는 발판처럼 "정해진 경로" 를 가는 물체
//   - MovePosition = 물리 엔진에 "이번 스텝에 여기로 간다" 를 알림 → 엔진이 그 이동을 속도로 해석
//     → 올라탄 상자·공을 밀어 줌 (transform.position 대입과의 차이)
//   - Interpolate 설정을 따름 → 화면에서 부드러움
//
// ⚠ 주의 : Kinematic 물체는 힘·충돌에 밀리지 않음 = 스스로는 벽에 "막히지 않음"
//   → 벽에서 멈춰야 하면 blockByWalls 를 켜서 SweepTest 로 미리 검사
//   → 벽에 막혀야 하는 플레이어라면 RigidbodyMover(동적) 또는 CharacterController 사용
//
// Unity 문서 : MovePosition 은 Kinematic Rigidbody 용으로 설계됨
// 사용법 : 발판(Box)에 Rigidbody(Is Kinematic 체크) + 이 스크립트 · 두 지점 a, b 지정
// ============================================================
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class KinematicMover : MonoBehaviour
{
    public Vector3 a = new Vector3(0, 0.5f, 0);
    public Vector3 b = new Vector3(0, 0.5f, 6);
    public float speed = 2f;            // m/s
    public bool blockByWalls = false;   // 켜면 진행 방향에 벽이 있을 때 그 앞에서 정지
    public float skin = 0.01f;          // 벽과 남길 간격

    Rigidbody rb;
    Vector3 target;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();
        rb.isKinematic = true;
        rb.interpolation = RigidbodyInterpolation.Interpolate;
        rb.position = a;
        target = b;
    }

    void FixedUpdate()
    {
        Vector3 next = Vector3.MoveTowards(rb.position, target, speed * Time.fixedDeltaTime);
        Vector3 delta = next - rb.position;

        if (blockByWalls && delta.sqrMagnitude > 0f &&
            rb.SweepTest(delta.normalized, out RaycastHit hit, delta.magnitude))
        {
            // 이동 경로에 무언가 있음 → 닿기 직전까지만
            next = rb.position + delta.normalized * Mathf.Max(0f, hit.distance - skin);
        }

        rb.MovePosition(next);   // ← transform.position 대입 대신

        if ((target - next).sqrMagnitude < 1e-6f)
            target = target == b ? a : b;   // 끝에 닿으면 왕복
    }
}
