// ============================================================
// 6주차 스타터 — 진단 스크립트  (검증 리포트용 로그 생성)
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 씬의 모든 Renderer 를 훑어
//   · 밉맵 없는 텍스처 (mipmapCount == 1)
//   · Point 필터 텍스처
//   · 투명 큐 재질 (renderQueue >= 3000)
// 를 찾아 Console 에 출력하고, 120 프레임 평균 프레임타임(ms)을 기록.
//
// 사용법 : 아무 GameObject 에 추가 → Play → Console 로그를 리포트에 복사
//          Inspector 우클릭 메뉴(⋮) «Run Audit Now» 로 다시 실행 가능
// ============================================================
using System.Collections.Generic;
using UnityEngine;

public class W06Audit : MonoBehaviour
{
    [Tooltip("Play 시작 후 몇 초 뒤 점검할지 (씬 생성 스크립트가 먼저 돌도록)")]
    public float delaySeconds = 1f;
    public int frameWindow = 120;

    float sum; int count;

    void Start() { Invoke(nameof(RunAudit), delaySeconds); }

    [ContextMenu("Run Audit Now")]
    public void RunAudit()
    {
        int noMip = 0, point = 0, transparent = 0;
        var seenTex = new HashSet<Texture>();
        var seenMat = new HashSet<Material>();

        foreach (var r in FindObjectsByType<Renderer>(FindObjectsSortMode.None))
        {
            foreach (var m in r.sharedMaterials)
            {
                if (m == null || !seenMat.Add(m)) continue;

                if (m.renderQueue >= 3000)
                {
                    transparent++;
                    Debug.Log($"[Audit] 투명 큐 재질 : {m.name} (queue {m.renderQueue}) · 예 : {r.name}");
                }

                // URP Lit 의 _BaseMap 은 [MainTexture] → mainTexture 로 조회됨
                if (m.mainTexture is Texture2D t && seenTex.Add(t))
                {
                    if (t.mipmapCount <= 1)
                    {
                        noMip++;
                        Debug.LogWarning($"[Audit] 밉맵 없음 : {t.name} ({t.width}×{t.height}) · 재질 {m.name}");
                    }
                    if (t.filterMode == FilterMode.Point)
                    {
                        point++;
                        Debug.LogWarning($"[Audit] Point 필터 : {t.name} · 재질 {m.name}");
                    }
                }
            }
        }
        Debug.Log($"[Audit] 요약 — 밉맵 없음 {noMip} · Point 필터 {point} · 투명 큐 재질 {transparent} · 점검 재질 {seenMat.Count}");
    }

    void Update()
    {
        sum += Time.unscaledDeltaTime; count++;
        if (count >= frameWindow)
        {
            Debug.Log($"[Audit] 프레임타임 평균 {sum / count * 1000f:F2} ms ({count} 프레임)");
            sum = 0; count = 0;
        }
    }
}
