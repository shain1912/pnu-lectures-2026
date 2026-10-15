// ============================================================
// 6주차 스타터 — 정답본  (AI 함정 #5 수정)
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 재현본(W06TrapTextureAlpha)과 같은 씬을 만들되
//   ① 바닥 텍스처 : 밉맵 생성 + Trilinear + 이방성 필터
//   ② 나뭇잎 : Transparent(알파 블렌딩) → Opaque + Alpha Clipping
// 으로 고친 버전. Play 중에 Inspector 에서 프리셋을 바꿔 A/B 비교 가능.
//
// 사용법
//   1) 재현본과 다른 빈 씬에 빈 GameObject 생성 → 이 스크립트 추가 → Play
//   2) Inspector 의 Floor Preset · Leaf Mode 를 Play 중에 바꿔 가며 같은 지점 비교
//   3) 비교 결과를 워크북 표에 기록
// ============================================================
using UnityEngine;
using UnityEngine.Rendering;

public class W06FixedTextureAlpha : MonoBehaviour
{
    public enum FloorPreset
    {
        PointNoMip,          // 재현본과 같은 상태 (비교용)
        BilinearNoMip,       // 필터만 바꾼 상태 — 여전히 반짝임
        TrilinearMip,        // 밉맵 + Trilinear — 반짝임 해결, 먼 곳 흐림
        TrilinearMipAniso    // + 이방성 — 먼 바닥 선명도 회복 (권장)
    }
    public enum LeafMode { AlphaBlend, AlphaClip }

    [Header("비교 스위치 (Play 중 변경 가능)")]
    public FloorPreset floorPreset = FloorPreset.TrilinearMipAniso;
    public LeafMode leafMode = LeafMode.AlphaClip;
    [Range(1, 16)] public int anisoLevel = 4;
    [Range(0.05f, 0.95f)] public float alphaClipThreshold = 0.5f;

    [Header("바닥")]
    public int textureSize = 1024;
    public int checksPerSide = 16;
    public float floorSize = 400f;
    public float tiling = 100f;

    [Header("나뭇잎 덤불")]
    public int bushCount = 6;
    public int cardsPerBush = 10;

    [Header("카메라 움직임 (증상 관찰용)")]
    public bool moveCamera = true;
    public float dollyRange = 3f;
    public float jitterArcmin = 3f;

    Texture2D texNoMip, texMip;
    Material floorMat, leafMat;
    Transform cam;
    Vector3 camBasePos;
    Quaternion camBaseRot;
    FloorPreset appliedFloor = (FloorPreset)(-1);
    LeafMode appliedLeaf = (LeafMode)(-1);
    int appliedAniso = -1;
    float appliedClip = -1f;

    void Start()
    {
        // 같은 무늬로 텍스처 두 벌 : 밉맵 없음 / 있음 (밉맵 유무는 생성 후 바꿀 수 없음)
        texNoMip = MakeChecker(false);
        texMip = MakeChecker(true);

        var floor = GameObject.CreatePrimitive(PrimitiveType.Plane);
        floor.name = "Floor (Fixed)";
        floor.transform.localScale = Vector3.one * (floorSize / 10f);
        floorMat = new Material(Shader.Find("Universal Render Pipeline/Lit"));
        floorMat.SetTextureScale("_BaseMap", new Vector2(tiling, tiling));
        floorMat.SetFloat("_Smoothness", 0.1f);
        floor.GetComponent<Renderer>().sharedMaterial = floorMat;

        leafMat = new Material(Shader.Find("Universal Render Pipeline/Lit"));
        leafMat.SetTexture("_BaseMap", MakeLeafTexture(256));
        leafMat.SetColor("_BaseColor", new Color(0.55f, 0.85f, 0.35f, 1f));
        BuildBushes();

        if (Camera.main != null)
        {
            cam = Camera.main.transform;
            cam.position = new Vector3(0f, 1.6f, -6f);
            cam.rotation = Quaternion.Euler(6f, 0f, 0f);
            camBasePos = cam.position;
            camBaseRot = cam.rotation;
        }
        ApplyIfChanged();
    }

    Texture2D MakeChecker(bool mip)
    {
        // ① mipChain = true → 축소판 레벨 생성 (1024 → 512 → … → 1)
        var tex = new Texture2D(textureSize, textureSize, TextureFormat.RGBA32, mip);
        tex.wrapMode = TextureWrapMode.Repeat;
        int cell = textureSize / checksPerSide;
        var px = new Color32[textureSize * textureSize];
        var white = new Color32(230, 234, 240, 255);
        var black = new Color32(20, 24, 32, 255);
        for (int y = 0; y < textureSize; y++)
            for (int x = 0; x < textureSize; x++)
                px[y * textureSize + x] = (((x / cell) + (y / cell)) & 1) == 0 ? white : black;
        tex.SetPixels32(px);
        // ② Apply(updateMipmaps: true) → 레벨 0 내용으로 축소판을 평균 계산해 채움
        tex.Apply(true);
        tex.name = mip ? "Checker_Mip" : "Checker_NoMip";
        return tex;
    }

    void ApplyIfChanged()
    {
        if (floorMat == null) return;
        if (floorPreset != appliedFloor || anisoLevel != appliedAniso)
        {
            Texture2D t;
            switch (floorPreset)
            {
                case FloorPreset.PointNoMip:
                    t = texNoMip; t.filterMode = FilterMode.Point; t.anisoLevel = 0; break;
                case FloorPreset.BilinearNoMip:
                    t = texNoMip; t.filterMode = FilterMode.Bilinear; t.anisoLevel = 0; break;
                case FloorPreset.TrilinearMip:
                    t = texMip; t.filterMode = FilterMode.Trilinear; t.anisoLevel = 0; break;
                default:
                    t = texMip; t.filterMode = FilterMode.Trilinear; t.anisoLevel = anisoLevel; break;
            }
            floorMat.SetTexture("_BaseMap", t);
            appliedFloor = floorPreset; appliedAniso = anisoLevel;
            Debug.Log($"[W06] 바닥 : {floorPreset} · mipmapCount = {t.mipmapCount} · filter = {t.filterMode} · aniso = {t.anisoLevel}");
        }
        if (leafMode != appliedLeaf || !Mathf.Approximately(alphaClipThreshold, appliedClip))
        {
            if (leafMode == LeafMode.AlphaClip) MakeCutout(leafMat, alphaClipThreshold);
            else MakeTransparent(leafMat);
            appliedLeaf = leafMode; appliedClip = alphaClipThreshold;
            Debug.Log($"[W06] 잎 : {leafMode} · renderQueue = {leafMat.renderQueue}");
        }
    }

    // 잎 · 철망처럼 «구멍만 뚫리면 되는» 재질 → 불투명 + 알파 클리핑
    static void MakeCutout(Material m, float threshold)
    {
        m.SetFloat("_Surface", 0f);                 // Opaque
        m.SetFloat("_AlphaClip", 1f);
        m.SetFloat("_Cutoff", threshold);           // 알파 < threshold 인 픽셀은 버림
        m.SetFloat("_Cull", (float)CullMode.Off);   // 얇은 카드 → 양면
        m.SetFloat("_ZWrite", 1f);                  // 깊이 기록 → 순서 문제 해결
        m.SetFloat("_SrcBlend", (float)BlendMode.One);
        m.SetFloat("_DstBlend", (float)BlendMode.Zero);
        m.SetFloat("_SrcBlendAlpha", (float)BlendMode.One);
        m.SetFloat("_DstBlendAlpha", (float)BlendMode.Zero);
        m.SetOverrideTag("RenderType", "TransparentCutout");
        m.DisableKeyword("_SURFACE_TYPE_TRANSPARENT");
        m.EnableKeyword("_ALPHATEST_ON");
        m.renderQueue = (int)RenderQueue.AlphaTest;  // 2450
    }

    // 비교용 : 재현본과 같은 알파 블렌딩
    static void MakeTransparent(Material m)
    {
        m.SetFloat("_Surface", 1f);
        m.SetFloat("_Blend", 0f);
        m.SetFloat("_AlphaClip", 0f);
        m.SetFloat("_Cull", (float)CullMode.Off);
        m.SetFloat("_ZWrite", 0f);
        m.SetFloat("_SrcBlend", (float)BlendMode.SrcAlpha);
        m.SetFloat("_DstBlend", (float)BlendMode.OneMinusSrcAlpha);
        m.SetFloat("_SrcBlendAlpha", (float)BlendMode.One);
        m.SetFloat("_DstBlendAlpha", (float)BlendMode.OneMinusSrcAlpha);
        m.SetOverrideTag("RenderType", "Transparent");
        m.DisableKeyword("_ALPHATEST_ON");
        m.EnableKeyword("_SURFACE_TYPE_TRANSPARENT");
        m.renderQueue = (int)RenderQueue.Transparent;  // 3000
    }

    void BuildBushes()
    {
        var rnd = new System.Random(6);   // 재현본과 같은 배치
        for (int b = 0; b < bushCount; b++)
        {
            var center = new Vector3(-6f + b * 2.4f, 0.8f, 2f + (b % 2) * 2.5f);
            for (int i = 0; i < cardsPerBush; i++)
            {
                var q = GameObject.CreatePrimitive(PrimitiveType.Quad);
                q.name = $"Leaf {b}-{i}";
                Destroy(q.GetComponent<Collider>());
                q.transform.position = center + new Vector3(
                    (float)(rnd.NextDouble() - 0.5) * 0.8f,
                    (float)(rnd.NextDouble() - 0.5) * 0.8f,
                    (float)(rnd.NextDouble() - 0.5) * 0.8f);
                q.transform.rotation = Quaternion.Euler(
                    (float)rnd.NextDouble() * 40f - 20f,
                    (i % 2 == 0 ? 0f : 90f) + (float)rnd.NextDouble() * 30f,
                    0f);
                q.transform.localScale = Vector3.one * 1.1f;
                q.GetComponent<Renderer>().sharedMaterial = leafMat;
            }
        }
    }

    static Texture2D MakeLeafTexture(int size)
    {
        // 잎 텍스처도 밉맵 생성 — 멀리서 잎 가장자리 반짝임 방지
        var tex = new Texture2D(size, size, TextureFormat.RGBA32, true);
        tex.wrapMode = TextureWrapMode.Clamp;
        tex.filterMode = FilterMode.Trilinear;
        var px = new Color32[size * size];
        for (int y = 0; y < size; y++)
            for (int x = 0; x < size; x++)
            {
                float u = (x + 0.5f) / size * 2f - 1f, v = (y + 0.5f) / size * 2f - 1f;
                float d = Mathf.Sqrt(u * u / 0.45f + v * v);
                float a = Mathf.Clamp01((1f - d) * 6f);
                float vein = Mathf.Abs(u) < 0.03f ? 0.75f : 1f;
                byte g = (byte)(255 * vein);
                px[y * size + x] = new Color32(g, g, g, (byte)(255 * a));
            }
        tex.SetPixels32(px);
        tex.Apply(true);
        return tex;
    }

    void Update()
    {
        ApplyIfChanged();
        if (!moveCamera || cam == null) return;
        float t = Time.time;
        cam.position = camBasePos + cam.forward * Mathf.Sin(t * 0.3f) * dollyRange;
        float a = jitterArcmin / 60f;
        float yaw = a * (0.6f * Mathf.Sin(2f * Mathf.PI * 1.1f * t) + 0.4f * Mathf.Sin(2f * Mathf.PI * 2.9f * t + 1.3f));
        float pitch = a * (0.6f * Mathf.Sin(2f * Mathf.PI * 0.8f * t + 0.5f) + 0.4f * Mathf.Sin(2f * Mathf.PI * 3.3f * t));
        cam.rotation = camBaseRot * Quaternion.Euler(pitch, yaw, 0f);
    }
}
