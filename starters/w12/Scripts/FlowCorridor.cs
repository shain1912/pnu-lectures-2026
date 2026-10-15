// ============================================================
// 12주차 스타터 · 광학 흐름 복도 생성기
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 실행 시 앞쪽(+Z)으로 긴 복도를 만듦 : 좌우 기둥 + 바닥 가로 줄무늬
//   · 대비가 강한 기둥이 시야 가장자리를 빠르게 지나감 → 주변 광학 흐름 최대 (유발 요인 ③)
//   · combineStatic 켜면 StaticBatchingUtility 로 메시 결합 → Part I 의 정적 배칭 확인
//     (Game 뷰 Stats 의 Batches 를 켜고/끄고 비교)
//
// 준비물 : 머티리얼 2개 (URP/Lit 또는 URP/Unlit) — 기둥용 밝은 색 · 바닥 줄무늬용
//          비워 두면 Shader.Find 로 임시 생성 (빌드에서 셰이더가 빠질 수 있으므로 지정 권장)
// ============================================================
using UnityEngine;

public class FlowCorridor : MonoBehaviour
{
    public Material pillarMaterial;
    public Material stripeMaterial;

    [Header("치수 (m)")]
    public float length = 80f;
    public float halfWidth = 1.6f;
    public float spacing = 1.5f;
    public float pillarHeight = 2.6f;
    public float pillarSize = 0.25f;

    [Header("배칭")]
    [Tooltip("생성 후 정적 배칭으로 결합 (Batches 감소 확인용)")]
    public bool combineStatic = true;

    void Start()
    {
        if (pillarMaterial == null) pillarMaterial = Fallback(new Color(1f, 0.37f, 0.64f));
        if (stripeMaterial == null) stripeMaterial = Fallback(new Color(0.21f, 0.84f, 0.9f));

        var root = new GameObject("FlowCorridor_Geometry").transform;
        root.SetParent(transform, false);

        for (float z = 0f; z <= length; z += spacing)
        {
            Box(root, new Vector3(-halfWidth, pillarHeight * 0.5f, z), new Vector3(pillarSize, pillarHeight, pillarSize), pillarMaterial);
            Box(root, new Vector3(halfWidth, pillarHeight * 0.5f, z), new Vector3(pillarSize, pillarHeight, pillarSize), pillarMaterial);
            Box(root, new Vector3(0f, 0.005f, z), new Vector3(halfWidth * 2f, 0.01f, 0.12f), stripeMaterial);
        }

        if (combineStatic) StaticBatchingUtility.Combine(root.gameObject);
    }

    static void Box(Transform parent, Vector3 pos, Vector3 scale, Material m)
    {
        var go = GameObject.CreatePrimitive(PrimitiveType.Cube);
        go.transform.SetParent(parent, false);
        go.transform.localPosition = pos;
        go.transform.localScale = scale;
        go.GetComponent<Renderer>().sharedMaterial = m;
        go.GetComponent<Renderer>().shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
    }

    static Material Fallback(Color c)
    {
        var sh = Shader.Find("Universal Render Pipeline/Unlit");
        if (sh == null) sh = Shader.Find("Universal Render Pipeline/Lit");
        var m = new Material(sh);
        if (m.HasProperty("_BaseColor")) m.SetColor("_BaseColor", c); else m.color = c;
        Debug.LogWarning("[FlowCorridor] 머티리얼 미지정 → 임시 생성. 빌드 전 머티리얼을 지정할 것");
        return m;
    }
}
