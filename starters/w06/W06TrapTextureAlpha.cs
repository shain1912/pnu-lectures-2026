// ============================================================
// 6주차 스타터 — 함정 재현본  (AI 함정 #5)
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// «멀리까지 펼쳐진 선명한 바둑판 바닥과, 그 위에 나뭇잎 덤불을 만들어 줘.
//   잎은 투명한 부분이 있으니 투명하게 처리해 줘.»
// 라는 요청에 AI 가 실제로 내놓을 법한 코드를 그대로 옮긴 것.
//
// 사용법
//   1) Unity 6 · URP 3D 프로젝트의 빈 씬에 빈 GameObject 생성
//   2) 이 스크립트 추가 → Play
//   3) 수정하지 말고 먼저 «증상» 부터 관찰 · 녹화 (워크북 실습 1)
//
// 주의 : 컴파일 오류·경고 없음. 에디터 정지 화면에서는 멀쩡해 보임.
// ============================================================
using UnityEngine;
using UnityEngine.Rendering;

public class W06TrapTextureAlpha : MonoBehaviour
{
    [Header("바닥")]
    public int textureSize = 1024;      // 텍스처 한 변 픽셀 수
    public int checksPerSide = 16;      // 텍스처 한 장 안의 칸 수 (한 변)
    public float floorSize = 400f;      // 바닥 한 변 길이 (m)
    public float tiling = 100f;         // 바닥에 텍스처 반복 횟수

    [Header("나뭇잎 덤불")]
    public int bushCount = 6;
    public int cardsPerBush = 10;

    [Header("카메라 움직임 (증상 관찰용)")]
    public bool moveCamera = true;
    [Tooltip("앞뒤 왕복 이동 폭 (m)")] public float dollyRange = 3f;
    [Tooltip("머리 미세 진동 흉내 · 각분(1/60°) 단위")] public float jitterArcmin = 3f;

    Transform cam;
    Vector3 camBasePos;
    Quaternion camBaseRot;

    void Start()
    {
        BuildFloor();
        BuildBushes();

        if (Camera.main != null)
        {
            cam = Camera.main.transform;
            cam.position = new Vector3(0f, 1.6f, -6f);
            cam.rotation = Quaternion.Euler(6f, 0f, 0f);
            camBasePos = cam.position;
            camBaseRot = cam.rotation;
        }
    }

    // ---------------------------------------------------------------- 바닥
    void BuildFloor()
    {
        // 선명한 바둑판을 위해 밉맵 없이 생성
        var tex = new Texture2D(textureSize, textureSize, TextureFormat.RGBA32, false);
        tex.filterMode = FilterMode.Point;          // 픽셀이 뭉개지지 않도록
        tex.wrapMode = TextureWrapMode.Repeat;

        int cell = textureSize / checksPerSide;
        var px = new Color32[textureSize * textureSize];
        var white = new Color32(230, 234, 240, 255);
        var black = new Color32(20, 24, 32, 255);
        for (int y = 0; y < textureSize; y++)
            for (int x = 0; x < textureSize; x++)
                px[y * textureSize + x] = (((x / cell) + (y / cell)) & 1) == 0 ? white : black;
        tex.SetPixels32(px);
        tex.Apply();

        var floor = GameObject.CreatePrimitive(PrimitiveType.Plane);
        floor.name = "Floor (Trap)";
        floor.transform.localScale = Vector3.one * (floorSize / 10f);   // Plane 기본 크기 10 m

        var mat = new Material(Shader.Find("Universal Render Pipeline/Lit"));
        mat.SetTexture("_BaseMap", tex);
        mat.SetTextureScale("_BaseMap", new Vector2(tiling, tiling));
        mat.SetFloat("_Smoothness", 0.1f);
        floor.GetComponent<Renderer>().sharedMaterial = mat;
    }

    // ---------------------------------------------------------------- 덤불
    void BuildBushes()
    {
        var leafTex = MakeLeafTexture(256);
        var mat = new Material(Shader.Find("Universal Render Pipeline/Lit"));
        mat.SetTexture("_BaseMap", leafTex);
        mat.SetColor("_BaseColor", new Color(0.55f, 0.85f, 0.35f, 1f));
        MakeTransparent(mat);   // 잎에 투명 부분이 있으니 투명 재질로

        var rnd = new System.Random(6);
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
                // 서로 교차하는 X 자 카드
                q.transform.rotation = Quaternion.Euler(
                    (float)rnd.NextDouble() * 40f - 20f,
                    (i % 2 == 0 ? 0f : 90f) + (float)rnd.NextDouble() * 30f,
                    0f);
                q.transform.localScale = Vector3.one * 1.1f;
                q.GetComponent<Renderer>().sharedMaterial = mat;
            }
        }
    }

    static void MakeTransparent(Material m)
    {
        m.SetFloat("_Surface", 1f);   // 0 Opaque · 1 Transparent
        m.SetFloat("_Blend", 0f);     // Alpha
        m.SetFloat("_Cull", (float)CullMode.Off);
        m.SetFloat("_ZWrite", 0f);
        m.SetFloat("_SrcBlend", (float)BlendMode.SrcAlpha);
        m.SetFloat("_DstBlend", (float)BlendMode.OneMinusSrcAlpha);
        m.SetFloat("_SrcBlendAlpha", (float)BlendMode.One);
        m.SetFloat("_DstBlendAlpha", (float)BlendMode.OneMinusSrcAlpha);
        m.SetOverrideTag("RenderType", "Transparent");
        m.EnableKeyword("_SURFACE_TYPE_TRANSPARENT");
        m.renderQueue = (int)RenderQueue.Transparent;
    }

    // 타원형 잎 모양 · 가장자리는 부드럽게 (알파 0 ~ 1)
    static Texture2D MakeLeafTexture(int size)
    {
        var tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
        tex.wrapMode = TextureWrapMode.Clamp;
        var px = new Color32[size * size];
        for (int y = 0; y < size; y++)
            for (int x = 0; x < size; x++)
            {
                float u = (x + 0.5f) / size * 2f - 1f, v = (y + 0.5f) / size * 2f - 1f;
                float d = Mathf.Sqrt(u * u / 0.45f + v * v);                 // 세로로 긴 타원
                float a = Mathf.Clamp01((1f - d) * 6f);
                float vein = Mathf.Abs(u) < 0.03f ? 0.75f : 1f;              // 가운데 잎맥
                byte g = (byte)(255 * vein);
                px[y * size + x] = new Color32(g, g, g, (byte)(255 * a));
            }
        tex.SetPixels32(px);
        tex.Apply();
        return tex;
    }

    // ---------------------------------------------------------------- 카메라
    void Update()
    {
        if (!moveCamera || cam == null) return;
        float t = Time.time;
        // 천천히 앞뒤 왕복 + 머리 미세 진동 (프레임과 무관하게 시간 기준)
        cam.position = camBasePos + cam.forward * Mathf.Sin(t * 0.3f) * dollyRange;
        float a = jitterArcmin / 60f;
        float yaw = a * (0.6f * Mathf.Sin(2f * Mathf.PI * 1.1f * t) + 0.4f * Mathf.Sin(2f * Mathf.PI * 2.9f * t + 1.3f));
        float pitch = a * (0.6f * Mathf.Sin(2f * Mathf.PI * 0.8f * t + 0.5f) + 0.4f * Mathf.Sin(2f * Mathf.PI * 3.3f * t));
        cam.rotation = camBaseRot * Quaternion.Euler(pitch, yaw, 0f);
    }
}
