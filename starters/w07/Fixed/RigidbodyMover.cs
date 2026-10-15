// ============================================================
// 7주차 · AI 함정 #6 정답본 ① — 동적 Rigidbody 를 "속도" 로 움직이기
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 핵심 : 위치를 덮어쓰지 않고 속도(linearVelocity)를 정함 → 위치·충돌은 물리 엔진이 계산
//   - 입력은 Update 에서 읽기 (키 누름을 놓치지 않도록)
//   - 물리 적용은 FixedUpdate 에서 (0.02초 고정 박자 · 3주차 실행 순서)
//   - 대시처럼 빠른 이동 → Collision Detection = Continuous Dynamic (터널링 방지)
//   - 화면 90Hz vs 물리 50Hz 떨림 → Interpolate
//
// Unity 6 : rb.velocity → rb.linearVelocity 로 이름 변경 (옛 이름은 Obsolete 경고)
// 사용법 : Sphere 에 Rigidbody + 이 스크립트 (TrapMover 는 제거) · Input System 패키지 사용
// ============================================================
using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(Rigidbody))]
public class RigidbodyMover : MonoBehaviour
{
    public float speed = 6f;
    public float dashSpeed = 40f;

    Rigidbody rb;
    Vector2 input;
    bool dash;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();
        rb.interpolation = RigidbodyInterpolation.Interpolate;                  // 화면 프레임 사이 보간
        rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;   // 이동 경로 전체 검사
        rb.constraints = RigidbodyConstraints.FreezeRotation;                   // 공이 굴러 방향이 틀어지지 않게
    }

    void Update()
    {
        input = ReadMove();
        dash = Keyboard.current != null && Keyboard.current.spaceKey.isPressed;
    }

    void FixedUpdate()
    {
        float s = dash ? dashSpeed : speed;
        Vector3 v = new Vector3(input.x, 0f, input.y) * s;
        v.y = rb.linearVelocity.y;      // 세로 속도(중력·낙하)는 물리 엔진 몫으로 유지
        rb.linearVelocity = v;          // 위치가 아니라 속도를 정함
    }

    static Vector2 ReadMove()
    {
        var k = Keyboard.current;
        if (k == null) return Vector2.zero;
        float x = (k.dKey.isPressed ? 1f : 0f) - (k.aKey.isPressed ? 1f : 0f);
        float y = (k.wKey.isPressed ? 1f : 0f) - (k.sKey.isPressed ? 1f : 0f);
        return Vector2.ClampMagnitude(new Vector2(x, y), 1f);
    }
}
