// ============================================================
// 7주차 · AI 함정 #6 재현본 — 일부러 틀리게 작성한 코드
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 상황 : "WASD 로 움직이는 공 만들어 줘" 라고만 요청했을 때 AI 가 흔히 내놓는 형태
// 증상 : ① 벽에 계속 밀면 부들부들 떨림  ② Space 대시 시 얇은 벽 통과
//        ③ 다른 Rigidbody 와 부딪혀도 상대가 거의 안 밀림
// 과제 : 증상을 재현 → 원인을 설명 → Fixed/RigidbodyMover.cs 와 비교
//
// 사용법 : Sphere 에 Rigidbody + 이 스크립트 · Unity 6 · Input System 패키지 사용
// ============================================================
using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(Rigidbody))]
public class TrapMover : MonoBehaviour
{
    public float speed = 6f;        // 걷기 m/s
    public float dashSpeed = 40f;   // 대시 m/s — 얇은 벽(0.2 m) 통과 재현용

    void Update()
    {
        Vector2 m = ReadMove();
        bool dash = Keyboard.current != null && Keyboard.current.spaceKey.isPressed;
        float s = dash ? dashSpeed : speed;

        Vector3 dir = new Vector3(m.x, 0f, m.y);

        // ▼ 함정 : Rigidbody 가 붙은 물체의 위치를 직접 덮어씀 (= 순간이동)
        //   - deltaTime 은 곱했으므로 3주차 함정 #2 는 통과한 코드
        //   - 그러나 rb 의 속도(linearVelocity)는 0 그대로 → 물리 엔진은 "속도 0 인 물체가 벽 속에 있음" 으로만 인식
        //   - Update(화면 시계)에서 실행 → 물리 스텝(0.02초) 사이에 여러 번 순간이동 → 경로 검사(CCD) 무의미
        transform.position += dir * s * Time.deltaTime;
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
