// ============================================================
//  11주 · AI 함정 #8 정답 — 카메라 말고 리그(XR Origin)를 옮긴다
//  컴퓨터그래픽스 VF3500076
//
//  요청 : "A 버튼을 누르면 다음 관찰 지점으로 시점 이동"
//  원칙
//   - Main Camera 의 Transform 은 «읽기 전용» — 값의 주인은 Tracked Pose Driver
//   - 이동·회전은 XR Origin(리그 루트)에 요청
//       1순위 : TeleportationProvider.QueueTeleportRequest
//               (XRI 3.x 에서 Locomotion Mediator 를 거쳐 리그를 이동
//                → 텔레포트·스냅 턴 등 다른 이동 기능과 충돌하지 않음)
//       2순위 : XROrigin.MoveCameraToWorldLocation (Locomotion 이 없는 단순 프로젝트)
//   - 보간·가속 없이 순간 이동 (12주 AI 함정 #9 : 부드러운 가속 이동 = 멀미)
//   - 눈높이 숫자를 코드에 쓰지 않음 (Tracking Origin Mode = Floor 가 실제 눈높이를 줌)
//
//  필요 패키지 : XR Interaction Toolkit 3.x (XR Core Utils 포함) · Input System
//  XRI 2.x 를 쓰는 경우 : 아래 Locomotion.Teleportation using 줄을 지우면 대부분 컴파일됨
// ============================================================
using UnityEngine;
using UnityEngine.InputSystem;
using Unity.XR.CoreUtils;
using UnityEngine.XR.Interaction.Toolkit;
using UnityEngine.XR.Interaction.Toolkit.Locomotion.Teleportation;

public class Fix_RigTeleportToSpot : MonoBehaviour
{
    [Tooltip("XR Origin (XR Rig) → Locomotion → Teleportation 에 있는 컴포넌트")]
    [SerializeField] TeleportationProvider teleportationProvider;

    [Tooltip("TeleportationProvider 가 없을 때만 사용하는 대체 경로")]
    [SerializeField] XROrigin xrOrigin;

    [Tooltip("다음 관찰 지점으로 이동할 버튼 액션 (예 : 오른손 A 버튼에 바인딩한 액션)")]
    [SerializeField] InputActionReference nextSpotAction;

    [Tooltip("관찰 지점들 — 바닥 위에 빈 오브젝트로 배치, 파란 화살표(forward) = 바라볼 방향")]
    [SerializeField] Transform[] spots;

    [Tooltip("검증 로그 : 카메라 로컬값이 이동 순간에도 연속인가")]
    [SerializeField] bool logContinuity = true;

    int index = -1;
    Transform cam;
    Vector3 prevLocal;

    void OnEnable()
    {
        if (nextSpotAction != null) nextSpotAction.action.Enable();
    }

    void Start()
    {
        if (xrOrigin == null) xrOrigin = FindAnyObjectByType<XROrigin>();
        cam = xrOrigin != null && xrOrigin.Camera != null ? xrOrigin.Camera.transform : Camera.main.transform;
        prevLocal = cam.localPosition;
    }

    void Update()
    {
        bool pressed =
            (nextSpotAction != null && nextSpotAction.action.WasPressedThisFrame()) ||
            (Keyboard.current != null && Keyboard.current.nKey.wasPressedThisFrame);   // 에디터 테스트용 N 키
        if (!pressed || spots == null || spots.Length == 0) return;

        index = (index + 1) % spots.Length;
        Transform spot = spots[index];

        if (teleportationProvider != null)
        {
            // ✔ 리그 루트를 옮겨 달라고 «요청» — 실제 이동은 Locomotion Mediator 가 순서대로 처리
            var request = new TeleportRequest
            {
                destinationPosition = spot.position,          // 발이 놓일 바닥 위치
                destinationRotation = spot.rotation,
                matchOrientation    = MatchOrientation.TargetUpAndForward
            };
            teleportationProvider.QueueTeleportRequest(request);
        }
        else if (xrOrigin != null)
        {
            // ✔ 대체 경로 : 카메라가 목표 지점 위에 오도록 XR Origin 을 이동
            //   현재 실제 눈높이(원점 기준 카메라 높이)는 그대로 유지
            float eyeHeight = cam.position.y - xrOrigin.transform.position.y;
            xrOrigin.MoveCameraToWorldLocation(spot.position + Vector3.up * eyeHeight);
            xrOrigin.MatchOriginUpCameraForward(spot.up, spot.forward);
        }
        else
        {
            Debug.LogWarning("[w11] TeleportationProvider 또는 XROrigin 을 연결할 것");
        }
    }

    void LateUpdate()
    {
        if (!logContinuity || cam == null) return;
        // 리그를 옮겨도 카메라의 «로컬» 값은 트래킹 값 그대로 → 이동 순간에도 연속
        // 1프레임 사이 5 cm 이상 튀면 누군가 카메라에 직접 쓰고 있다는 신호 (기준값은 예시)
        Vector3 lp = cam.localPosition;
        float jump = (lp - prevLocal).magnitude;
        if (jump > 0.05f)
            Debug.LogWarning($"[w11] 카메라 로컬값 튐 {jump:F3} m → 카메라 Transform 을 직접 쓰는 코드가 있는지 확인");
        prevLocal = lp;
    }
}
