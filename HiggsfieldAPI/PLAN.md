# Higgsfield API Integration Plan

## Goal
Build an app that accepts prompts and calls Higgsfield to generate images or videos.

---

## 1. Authentication

Higgsfield uses **API Key Bearer Token** authentication.

- Get API keys from: https://cloud.higgsfield.ai/api-keys
- SDK v2 format: `KEY_ID:KEY_SECRET`
- Environment variable: `HF_KEY="your-key-id:your-key-secret"`

```python
import os
os.environ["HF_KEY"] = "your-key-id:your-key-secret"
```

---

## 2. SDKs Available

| SDK | Install | Repo |
|-----|---------|------|
| Python | `pip install higgsfield-client` | https://github.com/higgsfield-ai/higgsfield-client |
| Node.js/TS | `npm install higgsfield-js` | https://github.com/higgsfield-ai/higgsfield-js |

**Recommendation:** Use the Python SDK for the initial app (simpler async handling).

---

## 3. API Capabilities (Pro Account)

### 3.1 Text-to-Image
- 50+ models available
- Key models: Flux, Flux Pro, SDXL, Seedream v4, Ideogram, Midjourney-style

**SDK pattern:**
```python
result = client.subscribe(
    'bytedance/seedream/v4/text-to-image',
    arguments={
        'prompt': 'your prompt here',
        'resolution': '2K',  # or '1K', '4K'
    }
)
image_url = result['images'][0]['url']
```

### 3.2 Image-to-Image
- 55+ models
- Features: style transfer, character preservation, enhancement/upscaling
- **Higgsfield Soul I2I**: 100+ preset styles from a single reference image

```python
result = client.subscribe(
    'higgsfield/soul/v1/image-to-image',
    arguments={
        'image_url': 'https://...',
        'style': 'preset_style_name',
        'prompt': 'optional modifier',
    }
)
```

### 3.3 Text-to-Video
- 70+ templates
- Key models: Kling 3.0, Veo 3.1, Wan 2.5, Sora 2, Seedance 2.0

```python
result = client.subscribe(
    'task/text-to-video',
    arguments={
        'prompt': 'cinematic scene description',
        'duration': 10,   # seconds
        'fps': 30,
        'resolution': '1080p',
    }
)
video_url = result['video']['url']
```

### 3.4 Image-to-Video
- Animates a static image with a motion prompt
- Supports 70+ animation templates

```python
result = client.subscribe(
    'task/image-to-video',
    arguments={
        'image_url': 'https://...',
        'prompt': 'slow zoom in, cinematic',
        'duration': 10,
        'fps': 30,
        'motion_intensity': 'medium',  # low | medium | high
    }
)
```

### 3.5 Lip Sync / Audio-Driven Video
- Models: LTX Lipsync, Infinite Talk
- Drive character mouth movement from audio

### 3.6 Audio & Voice Generation
- Text-to-speech and voice synthesis

---

## 4. Task Lifecycle

All tasks follow this flow:

```
submit() → Queued → InProgress → Completed | Failed | NSFW | Cancelled
```

**Polling approach:**
```python
request_id = client.submit('model/path', arguments={...})
status = client.status(request_id)   # poll until 'Completed'
result = client.result(request_id)
```

**Blocking approach (simpler):**
```python
result = client.subscribe('model/path', arguments={...})  # waits for completion
```

**Webhook approach (async):**
```python
result = client.subscribe('model/path', arguments={...}, webhook_url='https://yourapp/callback')
```

---

## 5. File Uploads

For image-to-image or image-to-video, upload local images first:

```python
image_url = client.upload_image('/path/to/local/image.jpg')
result = client.subscribe('task/image-to-video', arguments={'image_url': image_url, ...})
```

---

## 6. App Architecture Plan

```
User Input (prompt + mode selection)
        ↓
  App (Python / FastAPI or CLI)
        ↓
  HiggsfieldClient.subscribe(model, args)
        ↓
  Poll or wait for result
        ↓
  Display / save output (image URL or video URL)
```

### Phases
- **Phase 1 — CLI app**: Simple `python generate.py --mode image --prompt "..."` 
- **Phase 2 — Web app**: FastAPI backend + basic HTML frontend (prompt input, result display)
- **Phase 3 — Full UI**: Model selection, history, gallery of past generations

---

## 7. Pricing — BLOCKER

> **Status: On hold.** API access requires separate credits that are not included in any subscription plan.

### Subscription vs API Credits — Two Separate Systems

| | Web App (higgsfield.ai) | API (platform.higgsfield.ai) |
|--|------------------------|------------------------------|
| Credits | Included in subscription (e.g. 600/month on Pro) | **Separate purchase, starts at zero** |
| Cost | $29/month (Pro) | ~$10–15 per 100 credits, pay-as-you-go |
| Use case | Browser-based generation | Programmatic/SDK access |

**The Pro subscription ($29/month) only covers the web UI.** API credits must be purchased on top and are not bundled with any plan. This was confirmed by hitting a `403 Not enough credits` error despite having an active Pro subscription.

### Alternatives Worth Exploring

- **Segmind** (`api.segmind.com`) — third-party wrapper around Higgsfield models, per-generation pricing ($0.12–$4.22), may be cheaper for low-volume testing
- **Other video/image generation APIs** — Replicate, fal.ai, or RunwayML may offer better value with subscription-inclusive API access

---

## 8. Next Steps

- [x] Obtain API key from https://cloud.higgsfield.ai/api-keys
- [x] Install SDK: `pip install higgsfield-client`
- [x] Test connection — auth works, blocked by zero API credits
- [ ] Decide: purchase Higgsfield API credits, or switch to an alternative provider
- [ ] If switching, evaluate Replicate / fal.ai / RunwayML for equivalent image+video generation
