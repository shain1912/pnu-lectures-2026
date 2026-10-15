// ============================================================
// 12주차 스타터 · 멀미 유발본 (AI 함정 #9 재현)
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 목적 : «부드러운 가속 이동» 이 왜 VR 에서 최악인지 직접 겪고 측정하기
// 주의 : 동의자 체험 전용 · 노출 최대 3분 (maxExposureSeconds) · 앉아서 체험
//        스포터가 옆에 있을 것 · «그만» 하면 즉시 Stop 버튼
//
// 켜져 있는 유발 요인 (슬라이드 «유발 요인 체크리스트» 번호)
//   ① 가속·감속 : SmoothDamp 로 0.8초에 걸쳐 가속 (평균 약 5 m/s²)
//   ② 회전     : 부드러운 연속 회전 90°/s (요 임계 평균 27.1°/s 의 약 3.3배)
//   ③ 넓은 흐름 : FlowCorridor 의 기둥·바닥 줄무늬와 함께 쓰면 주변 광학 흐름 최대
//   ⑥ 기준 부재 : 고정 격자 없음 (ComfortModeSwitcher 가 끔)
//
// 함정 #8 을 다시 밟지 않도록 카메라가 아니라 «리그(XR Origin)» 를 움직인다.
// ============================================================
using UnityEngine;
using UnityEngine.InputSystem;

public class SicknessLocomotion : MonoBehaviour
{
    [Header("리그 · 머리")]
    [Tooltip("XR Origin (리그 루트). 비우면 이 컴포넌트가 붙은 Transform")]
    public Transform rig;
    [Tooltip("Main Camera (HMD). 이동 방향과 회전 중심으로 사용")]
    public Transform head;

    [Header("입력 (autoDrive 가 꺼져 있을 때 사용)")]
    [Tooltip("예 : XRI Left Locomotion/Move (Vector2)")]
    public InputActionReference moveAction;
    [Tooltip("예 : XRI Right Locomotion/Turn (Vector2)")]
    public InputActionReference turnAction;
    [Tooltip("즉시 정지 버튼 (선택). 누르면 이 컴포넌트가 꺼짐")]
    public InputActionReference stopAction;

    [Header("유발 파라미터 — AI 원본 값")]
    public float maxSpeed = 4f;           // m/s
    public float smoothTime = 0.8f;       // SmoothDamp 가속·감속 시간 (초)
    public float smoothTurnSpeed = 90f;   // °/s

    [Header("자동 주행 — 체험자는 조작하지 않음 (조건 통일용)")]
    public bool autoDrive = true;
    [Tooltip("전진 → 정지 → 후진 → 정지 한 주기 (초)")]
    public float autoPeriod = 8f;
    [Tooltip("자동 좌우 회전 사용")]
    public bool autoTurn = true;

    [Header("안전")]
    [Tooltip("이 시간이 지나면 자동 정지 (초). 수업 규칙 : 180 이하")]
    public float maxExposureSeconds = 180f;

    Vector3 vel, velRate;
    float turnVel, turnRate;
    float t;
    CharacterController cc;

    public float Exposure => t;

    void Awake()
    {
        if (rig == null) rig = transform;
        if (head == null && Camera.main != null) head = Camera.main.transform;
        cc = rig.GetComponent<CharacterController>();
    }

    void OnEnable()
    {
        t = 0f; vel = Vector3.zero; velRate = Vector3.zero; turnVel = 0f; turnRate = 0f;
        Enable(moveAction); Enable(turnAction); Enable(stopAction);
    }

    static void Enable(InputActionReference r) { if (r != null && r.action != null) r.action.Enable(); }

    void Update()
    {
        float dt = Time.deltaTime;
        t += dt;

        // ---- 안전 정지 -------------------------------------------------
        bool stopPressed = stopAction != null && stopAction.action != null && stopAction.action.WasPressedThisFrame();
        if (stopPressed || t > maxExposureSeconds)
        {
            Debug.Log($"[SicknessLocomotion] 정지 · 노출 {t:F1}초 · 사유 {(stopPressed ? "버튼" : "시간 상한")}");
            enabled = false;
            return;
        }

        // ---- 목표 속도 ----------------------------------------------------
        Vector3 fwd = Flat(head != null ? head.forward : rig.forward);
        Vector3 right = Flat(head != null ? head.right : rig.right);
        Vector3 target;
        float turnInput;

        if (autoDrive)
        {
            // 주기의 앞 35% 전진 · 15% 정지 · 35% 후진 · 15% 정지 → 출발·정지가 자주 반복
            float p = Mathf.Repeat(t / autoPeriod, 1f);
            float dir = p < 0.35f ? 1f : p < 0.5f ? 0f : p < 0.85f ? -1f : 0f;
            target = Flat(rig.forward) * dir * maxSpeed;   // 리그 정면 기준 (머리를 돌려도 경로 유지)
            turnInput = autoTurn ? Mathf.Sin(t * 2f * Mathf.PI / (autoPeriod * 1.3f)) * 0.7f : 0f;
        }
        else
        {
            Vector2 m = Read(moveAction);
            target = (fwd * m.y + right * m.x) * maxSpeed;
            turnInput = Read(turnAction).x;
        }

        // ---- 함정 #9 의 핵심 : 가속 곡선 ----------------------------------
        vel = Vector3.SmoothDamp(vel, target, ref velRate, smoothTime);
        Move(vel * dt);

        // 회전도 부드럽게 (가속 포함)
        turnVel = Mathf.SmoothDamp(turnVel, turnInput * smoothTurnSpeed, ref turnRate, smoothTime * 0.5f);
        if (head != null) rig.RotateAround(head.position, Vector3.up, turnVel * dt);
        else rig.Rotate(0f, turnVel * dt, 0f);
    }

    void Move(Vector3 delta)
    {
        if (cc != null && cc.enabled) cc.Move(delta);
        else rig.position += delta;
    }

    static Vector3 Flat(Vector3 v) { v.y = 0f; return v.sqrMagnitude > 1e-6f ? v.normalized : Vector3.forward; }

    static Vector2 Read(InputActionReference r)
    {
        if (r == null || r.action == null) return Vector2.zero;
        return r.action.ReadValue<Vector2>();
    }
}
