// ============================================================
// 12주차 스타터 · 완화본 — 동적 컴포트 베그넷 + 암전(Fade)
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 리그가 움직이거나 돌 때만 시야 가장자리를 어둡게 좁힘 (Fernandes & Feiner 2016 의 «동적» 방식)
// 멈추면 다시 열림 → 정지 상태의 시야·프레즌스는 그대로
//
// 구현 원리 (원리 확인용 최소 구현)
//   · 카메라 앞 distance(0.3 m) 에 사각 판 2장 : 가장자리만 검은 «구멍 뚫린 판» + 전체 암전 판
//   · 구멍 크기는 텍스처 타일링으로 조절 (Tiling 이 클수록 구멍이 작아짐 · 바깥은 Clamp 로 검정 유지)
//
// 준비물 : Material 1개 — Shader «Universal Render Pipeline/Unlit», Surface Type = Transparent
//          (Project 창 → Create → Material → 위 설정 → overlayMaterial 칸에 끌어 넣기)
//
// 정식 대안 : XRI Starter Assets 의 «Tunneling Vignette» 프리팹 (TunnelingVignetteController)
// 예외 규칙 : 머리에 붙은 요소지만 «정보» 가 아니라 «가장자리 어둠» 뿐 → 10주 함정 #7 과 별개
//             글자·아이콘을 여기에 올리지 말 것
// ============================================================
using System.Collections;
using UnityEngine;

public class ComfortVignette : MonoBehaviour
{
    [Header("대상")]
    [Tooltip("Main Camera (HMD)")]
    public Transform head;
    [Tooltip("움직임 감지 대상 = XR Origin")]
    public Transform rig;
    [Tooltip("URP/Unlit · Transparent 머티리얼 (복제해서 사용)")]
    public Material overlayMaterial;

    [Header("베그넷")]
    public bool vignetteEnabled = true;
    [Tooltip("0 = 효과 없음 · 1 = 가장 좁게")]
    [Range(0f, 1f)] public float strength = 0.6f;
    [Tooltip("닫히는 시간 (초)")] public float easeIn = 0.15f;
    [Tooltip("열리는 시간 (초)")] public float easeOut = 0.3f;
    [Tooltip("이 속도(m/s) 이상이면 이동 중으로 판정")] public float moveThreshold = 0.05f;
    [Tooltip("이 회전 속도(°/s) 이상이면 회전 중으로 판정")] public float turnThreshold = 5f;

    [Header("배치")]
    [Tooltip("카메라에서 판까지 거리 (m) · Near Clip 보다 멀게")]
    public float distance = 0.3f;

    Material vigMat, fadeMat;
    Renderer vigR, fadeR;
    float current;        // 현재 베그넷 강도 0~1
    float fadeAlpha;      // 현재 암전 0~1
    Vector3 lastPos; float lastYaw;

    public bool IsActive => current > 0.01f;

    void Start()
    {
        if (head == null && Camera.main != null) head = Camera.main.transform;
        if (rig == null) rig = transform;
        if (overlayMaterial == null)
        {
            Debug.LogWarning("[ComfortVignette] overlayMaterial 미지정 → 베그넷·암전 비활성");
            enabled = false;
            return;
        }
        // 화면 전체(Quest 3 약 110°)를 덮도록 판 크기 결정 : 반폭 = d·tan(약 63°) ≈ 2d
        float size = distance * 4f;

        vigMat = new Material(overlayMaterial);
        vigMat.renderQueue = 4000;
        SetMap(vigMat, MakeHoleTexture(128));
        SetColor(vigMat, Color.black);
        vigR = MakeQuad("ComfortVignette_Hole", size, vigMat);

        fadeMat = new Material(overlayMaterial);
        fadeMat.renderQueue = 4001;
        SetMap(fadeMat, Texture2D.whiteTexture);
        SetColor(fadeMat, new Color(0f, 0f, 0f, 0f));
        fadeR = MakeQuad("ComfortVignette_Fade", size, fadeMat);
        fadeR.enabled = false;

        lastPos = rig.position; lastYaw = rig.eulerAngles.y;
    }

    Renderer MakeQuad(string name, float size, Material m)
    {
        var go = GameObject.CreatePrimitive(PrimitiveType.Quad);
        go.name = name;
        Destroy(go.GetComponent<Collider>());
        go.transform.SetParent(head, false);
        go.transform.localPosition = new Vector3(0f, 0f, distance);
        go.transform.localRotation = Quaternion.identity;
        go.transform.localScale = new Vector3(size, size, 1f);
        var r = go.GetComponent<Renderer>();
        r.sharedMaterial = m;
        r.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
        r.receiveShadows = false;
        return r;
    }

    // 가운데 투명 · 가장자리 검정 · 경계는 부드럽게 (smoothstep)
    static Texture2D MakeHoleTexture(int n)
    {
        var tex = new Texture2D(n, n, TextureFormat.RGBA32, false);
        tex.wrapMode = TextureWrapMode.Clamp;
        var px = new Color32[n * n];
        for (int y = 0; y < n; y++)
            for (int x = 0; x < n; x++)
            {
                float u = (x + 0.5f) / n * 2f - 1f, v = (y + 0.5f) / n * 2f - 1f;
                float r = Mathf.Sqrt(u * u + v * v);           // 가운데 0 · 변 중앙 1
                float a = Mathf.SmoothStep(0f, 1f, Mathf.InverseLerp(0.62f, 0.95f, r));
                px[y * n + x] = new Color32(0, 0, 0, (byte)(a * 255));
            }
        tex.SetPixels32(px);
        tex.Apply();
        return tex;
    }

    void LateUpdate()
    {
        float dt = Time.deltaTime;
        // ---- 리그 움직임 감지 (어느 이동 스크립트든 동작) -------------------
        float speed = dt > 0f ? (rig.position - lastPos).magnitude / dt : 0f;
        float yawRate = dt > 0f ? Mathf.Abs(Mathf.DeltaAngle(lastYaw, rig.eulerAngles.y)) / dt : 0f;
        lastPos = rig.position; lastYaw = rig.eulerAngles.y;
        bool moving = speed > moveThreshold || yawRate > turnThreshold;

        float target = (vignetteEnabled && moving) ? strength : 0f;
        float rate = target > current ? 1f / Mathf.Max(0.01f, easeIn) : 1f / Mathf.Max(0.01f, easeOut);
        current = Mathf.MoveTowards(current, target, rate * dt);

        // 강도 → 타일링 : 1(구멍이 시야 밖) ~ 2.2(시야 약 75° 만 남김)
        float k = Mathf.Lerp(1f, 2.2f, current);
        vigR.enabled = current > 0.01f;
        if (vigR.enabled) SetTiling(vigMat, k);
    }

    /// <summary>암전 : alpha 0 = 투명 · 1 = 완전 검정. BlinkTeleport 가 사용</summary>
    public IEnumerator Fade(float targetAlpha, float time)
    {
        if (fadeMat == null) yield break;
        fadeR.enabled = true;
        float start = fadeAlpha, t = 0f;
        while (t < time)
        {
            t += Time.deltaTime;
            fadeAlpha = Mathf.Lerp(start, targetAlpha, time > 0f ? t / time : 1f);
            SetColor(fadeMat, new Color(0f, 0f, 0f, fadeAlpha));
            yield return null;
        }
        fadeAlpha = targetAlpha;
        SetColor(fadeMat, new Color(0f, 0f, 0f, fadeAlpha));
        fadeR.enabled = fadeAlpha > 0.001f;
    }

    // ---- URP Unlit 속성 이름 (_BaseMap · _BaseColor) 우선, 없으면 기본 속성 ----
    static void SetMap(Material m, Texture t)
    {
        if (m.HasProperty("_BaseMap")) m.SetTexture("_BaseMap", t); else m.mainTexture = t;
    }
    static void SetColor(Material m, Color c)
    {
        if (m.HasProperty("_BaseColor")) m.SetColor("_BaseColor", c); else m.color = c;
    }
    static void SetTiling(Material m, float k)
    {
        // uv' = uv·k + (0.5 − 0.5k) → 가운데를 기준으로 확대
        Vector2 scale = new Vector2(k, k), offset = new Vector2(0.5f - 0.5f * k, 0.5f - 0.5f * k);
        if (m.HasProperty("_BaseMap")) { m.SetTextureScale("_BaseMap", scale); m.SetTextureOffset("_BaseMap", offset); }
        else { m.mainTextureScale = scale; m.mainTextureOffset = offset; }
    }
}
