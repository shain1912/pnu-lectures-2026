// ============================================================
//  11주 · AI 함정 #8 재현용 — 카메라 Transform 직접 조작
//  컴퓨터그래픽스 VF3500076
//
//  이 스크립트는 «AI 가 흔히 내놓는 틀린 코드» 를 그대로 재현한 것.
//  요청 : "A 버튼을 누르면 다음 관찰 지점으로 시점 이동하는 스크립트 만들어줘"
//
//  증상
//   - 에디터(헤드셋 없음)에서는 이동하는 것처럼 보임 (설정·버전에 따라 다름)
//   - 헤드셋 빌드에서는 제자리 · 또는 한 순간 깜빡이고 원위치
//  원인
//   - Main Camera 의 Tracked Pose Driver 가 매 프레임(Update 와 렌더 직전)
//     헤드셋 자세로 localPosition · localRotation 을 덮어씀
//   - 이 스크립트가 Update 에서 쓴 값은 렌더 직전에 사라짐
//  진단
//   - 콘솔 로그 : «지난 프레임에 쓴 값» 과 «이번 프레임 시작 값» 이 다르면 덮어쓰기 중
//  수정
//   - Fix_RigTeleportToSpot.cs 참고 (XR Origin 루트를 이동)
//
//  ※ AI 가 "Tracked Pose Driver 를 끄면 된다" 고 고치면 따르지 말 것
//    → 머리를 돌려도 세상이 따라 도는 최악의 감각 충돌 (즉각 멀미)
// ============================================================
using UnityEngine;
using UnityEngine.InputSystem;

public class Trap_CameraDirectMove : MonoBehaviour
{
    [Tooltip("다음 관찰 지점으로 이동할 버튼 액션 (예 : 오른손 A 버튼에 바인딩한 액션)")]
    [SerializeField] InputActionReference nextSpotAction;

    [Tooltip("관찰 지점들 — 바닥 위에 빈 오브젝트로 배치, 파란 화살표(forward) = 바라볼 방향")]
    [SerializeField] Transform[] spots;

    [Tooltip("덮어쓰기 진단 로그 출력")]
    [SerializeField] bool logOverwrite = true;

    Transform cam;
    int index = -1;
    bool wrote;
    Vector3 written;

    void OnEnable()
    {
        if (nextSpotAction != null) nextSpotAction.action.Enable();
    }

    void Start()
    {
        cam = Camera.main.transform;
    }

    void Update()
    {
        // ---- 진단 : 지난 프레임에 쓴 값이 살아남았는가 ----
        // LateUpdate 에서 비교하면 아직 같은 값으로 보임
        // → 덮어쓰기는 그 뒤(렌더 직전)에 일어나므로 «다음 프레임 시작» 에서 비교
        if (logOverwrite && wrote)
        {
            Vector3 now = cam.localPosition;
            float diff = (now - written).magnitude;
            Debug.Log($"[함정#8] 지난 프레임에 쓴 로컬값 {written.ToString("F3")} → 이번 프레임 시작 {now.ToString("F3")} · 차이 {diff:F3} m" +
                      (diff > 0.01f ? "  ← Tracked Pose Driver 가 덮어씀" : ""));
            wrote = false;
        }

        bool pressed =
            (nextSpotAction != null && nextSpotAction.action.WasPressedThisFrame()) ||
            (Keyboard.current != null && Keyboard.current.nKey.wasPressedThisFrame);   // 에디터 테스트용 N 키
        if (!pressed || spots == null || spots.Length == 0) return;

        index = (index + 1) % spots.Length;
        Transform spot = spots[index];

        // ✗ 함정 ① : 트래킹이 매 프레임 덮어쓰는 Main Camera 에 직접 씀
        // ✗ 함정 ② : 눈높이 1.6 m 를 코드에 숫자로 박음 (사람마다·원점 모드마다 다름)
        cam.position = spot.position + Vector3.up * 1.6f;
        cam.rotation = spot.rotation;

        written = cam.localPosition;
        wrote = true;
    }
}
