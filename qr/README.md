# QR assets for the CV

Generate AFTER first deploy (URL must be live):

- Target URL: `https://shihabarch.tech/ask?src=cv-qr`  (src param = scan tracking)
- Suggested generator: `qrencode -o qr/cv-qr.png -s 12 --margin=2 'https://shihabarch.tech/ask?src=cv-qr'`
  (or any generator; keep an SVG + PNG pair)
- Place on CV: header, next to contact block, caption: "Scan to ask my AI anything about my work"
- Re-generate if the ask page URL ever changes; keep old URL working via redirect.
