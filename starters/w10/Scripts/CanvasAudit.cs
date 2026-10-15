// 10주차 스타터 — 캔버스 점검 로거 (AI 함정 #7 진단 · 각크기 측정)
// 씬의 아무 오브젝트에 부착 → Play → 콘솔 확인 · 또는 컴포넌트 ⋮ 메뉴 → «Audit Now»
//
// 출력
//  - 모든 루트 Canvas 의 Render Mode · Scale
//  - World Space 캔버스 : 거리(m) · 정면 기준 좌우 각도(°) · 폭 각크기(°) · 글자 DMM(근사)
//  - 판정 : Overlay 존재 · 0.5 m 미만 · 2 m 초과 · ±30° 밖 · 글자 24 DMM 미만
//
// 공식
//  각크기 θ = 2·atan(s / 2d)      s : 실제 크기(m) · d : 거리(m)
//  DMM      = 크기(mm) ÷ 거리(m)   (1 m 거리에서의 mm 로 환산)

using UnityEngine;
using TMPro;

public class CanvasAudit : MonoBehaviour
{
    [SerializeField] Transform viewer;            // 비우면 Camera.main
    [SerializeField] float minDistance = 0.5f;
    [SerializeField] float maxDistance = 2.0f;
    [SerializeField] float maxYaw = 30f;
    [SerializeField] float minTextDmm = 24f;

    void Start() => Audit();

    [ContextMenu("Audit Now")]
    public void Audit()
    {
        var cam = viewer ? viewer : (Camera.main ? Camera.main.transform : null);
        int overlay = 0, warnings = 0;

        foreach (var c in FindObjectsByType<Canvas>(FindObjectsInactive.Include, FindObjectsSortMode.None))
        {
            if (!c.isRootCanvas) continue;
            var rt = (RectTransform)c.transform;
            string head = $"[Canvas] {c.name} : {c.renderMode} · scale {rt.lossyScale.x:0.####}";

            if (c.renderMode == RenderMode.ScreenSpaceOverlay)
            {
                overlay++;
                Debug.LogWarning(head + " → 헤드셋 렌즈 화면에 그려지지 않음 (함정 #7)");
                continue;
            }
            if (c.renderMode == RenderMode.ScreenSpaceCamera)
            {
                warnings++;
                Debug.LogWarning(head + $" · planeDistance {c.planeDistance} m → 머리 고정(헤드락)");
                continue;
            }
            if (cam == null) { Debug.Log(head + " · 기준 카메라 없음"); continue; }

            float w   = rt.rect.width * rt.lossyScale.x;                       // 실제 폭 (m)
            float d   = Vector3.Distance(cam.position, rt.position);           // 거리 (m)
            float deg = 2f * Mathf.Atan(w / (2f * d)) * Mathf.Rad2Deg;          // 폭 각크기
            Vector3 flatFwd = Vector3.ProjectOnPlane(cam.forward, Vector3.up);
            Vector3 flatTo  = Vector3.ProjectOnPlane(rt.position - cam.position, Vector3.up);
            float yaw = Vector3.SignedAngle(flatFwd, flatTo, Vector3.up);       // 정면 기준 좌우 각도

            // 가장 작은 글자 기준 · TMP fontSize 는 em 높이 → 실제 글자 높이와 차이 있음 (근사)
            float minDmm = float.MaxValue;
            foreach (var t in c.GetComponentsInChildren<TMP_Text>(true))
            {
                float mm = t.fontSize * t.transform.lossyScale.y * 1000f;
                minDmm = Mathf.Min(minDmm, mm / d);
            }

            string msg = head + $" · 거리 {d:F2} m · 정면에서 {yaw:F0}° · 폭 {w:F2} m = {deg:F1}°";
            if (minDmm < float.MaxValue) msg += $" · 최소 글자 {minDmm:F0} DMM";

            bool bad = false;
            if (d < minDistance) { msg += $" · ✕ {minDistance} m 미만"; bad = true; }
            if (d > maxDistance) { msg += $" · ✕ {maxDistance} m 초과"; bad = true; }
            if (Mathf.Abs(yaw) > maxYaw) { msg += $" · ✕ ±{maxYaw}° 밖"; bad = true; }
            if (minDmm < minTextDmm) { msg += $" · ✕ 글자 {minTextDmm} DMM 미만"; bad = true; }
            if (rt.lossyScale.x > 0.01f) { msg += " · ✕ Scale 과대 (0.001 권장)"; bad = true; }

            if (bad) { warnings++; Debug.LogWarning(msg); } else Debug.Log(msg + " · 통과");
        }
        Debug.Log($"[CanvasAudit] Overlay {overlay}개 · 경고 {warnings}개");
    }
}
