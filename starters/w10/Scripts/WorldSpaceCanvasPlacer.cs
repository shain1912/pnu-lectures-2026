// 10주차 스타터 — 캔버스를 «공간 UI» 로 배치 (또는 비교용 Overlay 로 되돌리기)
// Canvas 오브젝트에 부착 → 컴포넌트 ⋮ 메뉴
//   «Place World Space»  : World Space · 600×360 (= 0.6×0.36 m) · Scale 0.001 · 카메라 앞 distance m · 눈높이보다 약간 아래
//   «Make Overlay (함정)» : Screen Space Overlay 로 변경 — 11주차 헤드셋 비교용
//
// 숫자 근거 (10주차 Part II)
//   600 × 0.001 = 0.6 m · 360 × 0.001 = 0.36 m
//   폭 0.6 m 를 1.5 m 에서 보면 2·atan(0.3/1.5) ≈ 22.6°

using UnityEngine;

[RequireComponent(typeof(Canvas))]
public class WorldSpaceCanvasPlacer : MonoBehaviour
{
    [SerializeField] Transform viewer;                 // 비우면 Camera.main
    [SerializeField] Vector2 canvasUnits = new Vector2(600, 360);
    [SerializeField] float unitScale = 0.001f;         // 캔버스 1 단위 = 1 mm
    [SerializeField, Range(0.5f, 2f)] float distance = 1.5f;
    [SerializeField, Range(-30f, 30f)] float yawOffset = 0f;
    [SerializeField] float dropBelowEye = 0.15f;       // 눈높이보다 아래로 (m) — 시선이 약간 아래가 편함

    [ContextMenu("Place World Space")]
    public void PlaceWorldSpace()
    {
        var canvas = GetComponent<Canvas>();
        var cam = viewer ? viewer : (Camera.main ? Camera.main.transform : null);
        if (cam == null) { Debug.LogError("기준 카메라 없음 — Main Camera 태그 확인"); return; }

        canvas.renderMode = RenderMode.WorldSpace;
        var camComp = cam.GetComponent<Camera>();
        if (camComp) canvas.worldCamera = camComp;     // Event Camera

        var rt = (RectTransform)transform;
        rt.sizeDelta = canvasUnits;
        rt.localScale = Vector3.one * unitScale;

        Vector3 fwd = Vector3.ProjectOnPlane(cam.forward, Vector3.up).normalized;
        if (fwd.sqrMagnitude < 0.01f) fwd = Vector3.forward;
        fwd = Quaternion.Euler(0, yawOffset, 0) * fwd;
        rt.position = cam.position + fwd * distance + Vector3.down * dropBelowEye;
        // Unity UI 는 캔버스 +Z 가 카메라 반대쪽을 향할 때 앞면이 보임 → «카메라 → 패널» 방향을 forward 로
        // 패널이 눈보다 아래 → 자동으로 위쪽이 살짝 뒤로 기운 각도 = 시선과 수직
        rt.rotation = Quaternion.LookRotation(rt.position - cam.position, Vector3.up);

        TryAddTrackedDeviceRaycaster();

        float w = canvasUnits.x * unitScale;
        float deg = 2f * Mathf.Atan(w / (2f * distance)) * Mathf.Rad2Deg;
        Debug.Log($"[Placer] World Space · 폭 {w:F2} m · 거리 {distance:F2} m · 각크기 {deg:F1}° · 좌우 {yawOffset:F0}°");
    }

    [ContextMenu("Make Overlay (함정)")]
    public void MakeOverlay()
    {
        GetComponent<Canvas>().renderMode = RenderMode.ScreenSpaceOverlay;
        Debug.LogWarning("[Placer] Screen Space Overlay — 에디터에선 보이지만 헤드셋에선 그려지지 않음 (11주 비교용)");
    }

    // XR Interaction Toolkit 이 설치돼 있으면 Tracked Device Graphic Raycaster 자동 추가
    // (미설치 시 건너뜀 — 11주차 XRI 설치 후 다시 실행)
    void TryAddTrackedDeviceRaycaster()
    {
        var t = System.Type.GetType(
            "UnityEngine.XR.Interaction.Toolkit.UI.TrackedDeviceGraphicRaycaster, Unity.XR.Interaction.Toolkit");
        if (t == null) { Debug.Log("[Placer] XRI 미설치 — Tracked Device Graphic Raycaster 는 11주차에 추가"); return; }
        if (GetComponent(t) == null) gameObject.AddComponent(t);
    }
}
