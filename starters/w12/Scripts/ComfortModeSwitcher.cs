// ============================================================
// 12주차 스타터 · 유발본 ↔ 완화본 전환 (빌드 한 번으로 교차 체험)
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 스포터(진행자)가 버튼으로 모드를 바꿈 → 체험자는 조작하지 않음
//   Sickness : SicknessLocomotion 켬 · 완화 기능 전부 끔 · 고정 격자 끔
//   Comfort  : ComfortLocomotion + BlinkTeleport + ComfortVignette 켬 · 고정 격자 켬
// 에디터 테스트 : Tab 키로도 전환
// ============================================================
using UnityEngine;
using UnityEngine.InputSystem;

public class ComfortModeSwitcher : MonoBehaviour
{
    public enum Mode { Sickness, Comfort }

    [Header("시작 모드")]
    public Mode startMode = Mode.Comfort;   // 안전을 위해 기본은 완화본

    [Header("유발본")]
    public SicknessLocomotion sickness;

    [Header("완화본")]
    public ComfortLocomotion comfort;
    public BlinkTeleport teleport;
    public ComfortVignette vignette;
    [Tooltip("XR Origin 의 자식으로 둔 바닥 격자 등 «실제 방 기준» 고정 기준 (선택)")]
    public GameObject fixedReference;

    [Header("전환 입력 (선택)")]
    [Tooltip("예 : 왼쪽 컨트롤러 메뉴 버튼 · 스포터가 누름")]
    public InputActionReference switchAction;

    [Header("기록")]
    public MotionLogger logger;

    public Mode Current { get; private set; }

    void Start() { Apply(startMode); }

    void OnEnable()
    {
        if (switchAction != null && switchAction.action != null) switchAction.action.Enable();
    }

    void Update()
    {
        bool pressed = switchAction != null && switchAction.action != null && switchAction.action.WasPressedThisFrame();
        if (Keyboard.current != null && Keyboard.current.tabKey.wasPressedThisFrame) pressed = true;
        if (pressed) Apply(Current == Mode.Sickness ? Mode.Comfort : Mode.Sickness);
    }

    public void Apply(Mode m)
    {
        Current = m;
        bool s = m == Mode.Sickness;
        if (sickness != null) sickness.enabled = s;
        if (comfort != null) comfort.enabled = !s;
        if (teleport != null) teleport.enabled = !s;
        if (vignette != null) vignette.vignetteEnabled = !s;
        if (fixedReference != null) fixedReference.SetActive(!s);
        if (logger != null) logger.BeginSession(s ? "sickness" : "comfort");
        Debug.Log($"[ComfortModeSwitcher] 모드 = {m}");
    }
}
