// ============================================================
// 12주차 스타터 · 완화본 이동 — 블링크 텔레포트
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 버튼을 누르고 있는 동안 : 컨트롤러 정면으로 광선 → 바닥에 도착 표시
// 버튼을 놓으면       : 짧게 암전 (기본 0.15초) → 리그 이동 → 다시 밝아짐
// 이동 과정(광학 흐름)이 아예 없음 → 유발 요인 ① 가속 · ③ 흐름 제거
//
// · XRI 의 Teleportation Provider 를 써도 됨. 이 스크립트는 «원리 확인용» 최소 구현
// · 암전에는 ComfortVignette 의 Fade 기능 사용 (없으면 암전 없이 즉시 이동)
// ============================================================
using System.Collections;
using UnityEngine;
using UnityEngine.InputSystem;

public class BlinkTeleport : MonoBehaviour
{
    [Header("리그 · 머리 · 컨트롤러")]
    public Transform rig;
    public Transform head;
    [Tooltip("광선을 쏠 컨트롤러 Transform (예 : Right Controller)")]
    public Transform rayOrigin;

    [Header("입력")]
    [Tooltip("예 : XRI Right Locomotion/Teleport Mode · 버튼·스틱 모두 가능 (누름 판정)")]
    public InputActionReference teleportAction;

    [Header("목표 지점")]
    public LayerMask floorMask = ~0;
    public float maxDistance = 10f;
    [Tooltip("이 값보다 가파른 면에는 착지 불가 (법선 y)")]
    [Range(0f, 1f)] public float minFloorNormalY = 0.7f;
    [Tooltip("도착 지점 표시 (선택) — 바닥에 눕힌 원판 등")]
    public Transform marker;
    [Tooltip("광선 표시 (선택)")]
    public LineRenderer line;

    [Header("블링크")]
    public ComfortVignette fader;
    [Tooltip("암전 전체 시간 (초) · 절반은 어두워지기, 절반은 밝아지기")]
    public float blinkTime = 0.15f;

    bool wasPressed;
    bool hasTarget;
    Vector3 targetPoint;
    bool busy;
    CharacterController cc;

    void Awake()
    {
        if (rig == null) rig = transform;
        if (head == null && Camera.main != null) head = Camera.main.transform;
        cc = rig.GetComponent<CharacterController>();
        if (marker != null) marker.gameObject.SetActive(false);
        if (line != null) line.enabled = false;
    }

    void OnEnable()
    {
        if (teleportAction != null && teleportAction.action != null) teleportAction.action.Enable();
    }

    void OnDisable()
    {
        if (marker != null) marker.gameObject.SetActive(false);
        if (line != null) line.enabled = false;
        wasPressed = false;
    }

    void Update()
    {
        if (busy || rayOrigin == null || teleportAction == null || teleportAction.action == null) return;
        bool pressed = teleportAction.action.IsPressed();

        if (pressed) Aim();

        if (wasPressed && !pressed)
        {
            if (marker != null) marker.gameObject.SetActive(false);
            if (line != null) line.enabled = false;
            if (hasTarget) StartCoroutine(Blink(targetPoint));
        }
        wasPressed = pressed;
    }

    void Aim()
    {
        hasTarget = false;
        Vector3 o = rayOrigin.position, d = rayOrigin.forward;
        Vector3 end = o + d * maxDistance;
        if (Physics.Raycast(o, d, out RaycastHit hit, maxDistance, floorMask, QueryTriggerInteraction.Ignore)
            && hit.normal.y >= minFloorNormalY)
        {
            hasTarget = true;
            targetPoint = hit.point;
            end = hit.point;
        }
        if (marker != null)
        {
            marker.gameObject.SetActive(hasTarget);
            if (hasTarget) marker.position = targetPoint + Vector3.up * 0.01f;
        }
        if (line != null)
        {
            line.enabled = true;
            line.positionCount = 2;
            line.SetPosition(0, o);
            line.SetPosition(1, end);
        }
    }

    IEnumerator Blink(Vector3 point)
    {
        busy = true;
        float half = blinkTime * 0.5f;
        if (fader != null) yield return fader.Fade(1f, half);

        // 머리의 바닥 투영점이 목표 지점에 오도록 리그를 옮김
        // (리그 원점이 아니라 «사람이 서 있는 자리» 를 맞추는 것이 핵심)
        Vector3 headOnFloor = new Vector3(head.position.x, rig.position.y, head.position.z);
        Vector3 delta = point - headOnFloor;
        bool ccOn = cc != null && cc.enabled;
        if (ccOn) cc.enabled = false;          // CharacterController 는 위치 직접 대입을 덮어씀
        rig.position += delta;
        if (ccOn) cc.enabled = true;

        if (fader != null) yield return fader.Fade(0f, half);
        busy = false;
    }
}
