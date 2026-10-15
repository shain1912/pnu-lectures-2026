// ============================================================
// 12주차 스타터 · 완화본 이동 — 등속 · 즉시 전환 + 스냅 턴
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 유발본(SicknessLocomotion) 과 비교해 바뀐 점
//   ① 가속 곡선 없음 : 입력이 들어오면 그 프레임에 바로 speed, 놓으면 바로 0
//      → 가속은 «한 프레임에 한 번» 으로 끝남 (충돌 지속 시간 최소화)
//   ② 부드러운 회전 없음 : 스냅 턴 (기본 22.5° · Farmani & Teather 2018 조건)
//   · 이동 방향 = 머리 정면을 수평면에 투영한 방향
//   · 리그(XR Origin) 만 이동 · 카메라는 건드리지 않음 (함정 #8)
// ============================================================
using UnityEngine;
using UnityEngine.InputSystem;

public class ComfortLocomotion : MonoBehaviour
{
    [Header("리그 · 머리")]
    public Transform rig;
    public Transform head;

    [Header("입력")]
    [Tooltip("예 : XRI Left Locomotion/Move (Vector2)")]
    public InputActionReference moveAction;
    [Tooltip("예 : XRI Right Locomotion/Turn 또는 Snap Turn (Vector2) — x 값만 사용")]
    public InputActionReference turnAction;

    [Header("등속 이동")]
    [Tooltip("m/s · 전방 등속 임계 평균 1.183 m/s (Terenzi & Zaal 2020) 근처")]
    public float speed = 1.2f;
    [Range(0f, 0.5f)] public float deadZone = 0.15f;

    [Header("스냅 턴")]
    public float snapAngle = 22.5f;
    [Tooltip("스틱을 이 값 이상 밀면 한 번 회전")]
    [Range(0.3f, 0.95f)] public float snapThreshold = 0.7f;
    [Tooltip("연속 회전 사이 최소 간격 (초)")]
    public float snapCooldown = 0.25f;

    CharacterController cc;
    float lastSnap = -10f;
    bool stickArmed = true;   // 스틱이 가운데로 돌아와야 다음 스냅 허용

    /// <summary>이번 프레임에 이동 중인가 (베그넷 등에서 사용)</summary>
    public bool IsMoving { get; private set; }

    void Awake()
    {
        if (rig == null) rig = transform;
        if (head == null && Camera.main != null) head = Camera.main.transform;
        cc = rig.GetComponent<CharacterController>();
    }

    void OnEnable()
    {
        if (moveAction != null && moveAction.action != null) moveAction.action.Enable();
        if (turnAction != null && turnAction.action != null) turnAction.action.Enable();
    }

    void OnDisable() { IsMoving = false; }

    void Update()
    {
        // ---- 등속 · 즉시 전환 ---------------------------------------------
        Vector2 m = moveAction != null && moveAction.action != null ? moveAction.action.ReadValue<Vector2>() : Vector2.zero;
        if (m.magnitude < deadZone) m = Vector2.zero;
        else m = m.normalized;                       // 스틱을 얼마나 밀든 속도는 같음 → 속도 변화 = 0 또는 speed

        Vector3 fwd = Flat(head != null ? head.forward : rig.forward);
        Vector3 right = Flat(head != null ? head.right : rig.right);
        Vector3 v = (fwd * m.y + right * m.x) * speed; // SmoothDamp 없음
        IsMoving = v.sqrMagnitude > 1e-4f;
        if (IsMoving)
        {
            Vector3 delta = v * Time.deltaTime;
            if (cc != null && cc.enabled) cc.Move(delta); else rig.position += delta;
        }

        // ---- 스냅 턴 ------------------------------------------------------
        float x = turnAction != null && turnAction.action != null ? turnAction.action.ReadValue<Vector2>().x : 0f;
        if (Mathf.Abs(x) < 0.25f) stickArmed = true;
        if (stickArmed && Mathf.Abs(x) >= snapThreshold && Time.time - lastSnap >= snapCooldown)
        {
            float a = Mathf.Sign(x) * snapAngle;
            // 머리 위치를 중심으로 회전 → 몸이 옆으로 밀려 보이지 않음
            if (head != null) rig.RotateAround(head.position, Vector3.up, a);
            else rig.Rotate(0f, a, 0f);
            lastSnap = Time.time;
            stickArmed = false;
        }
    }

    static Vector3 Flat(Vector3 v) { v.y = 0f; return v.sqrMagnitude > 1e-6f ? v.normalized : Vector3.forward; }
}
