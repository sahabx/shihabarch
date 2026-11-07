# QR assets for the CV

Generated 2026-11-07 — target URL: `https://shihabarch.tech/ask?src=cv-qr` (src param = scan tracking, logged by the chat backend).

- `cv-qr.png` — dark-navy modules on white (screen)
- `cv-qr-black.png` — pure black (best for print)
- `cv-qr.svg` — vector

Regenerate (URL unchanged):
```bash
python3 -c "
import qrcode
from qrcode.image.svg import SvgPathImage
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=2)
qr.add_data('https://shihabarch.tech/ask?src=cv-qr'); qr.make(fit=True)
qr.make_image(fill_color='black', back_color='white').save('qr/cv-qr-black.png')
"
```

Place on CV: header, next to contact block, caption: **"Scan to ask my AI anything about my work"**
The /ask page works fully offline-of-backend (local retrieval) and upgrades to LLM answers once CHAT_API_URL is set.
