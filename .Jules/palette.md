## 2026-09-19 - Native System Dark Mode in Telegram Web Apps
**Learning:** In vanilla HTML/JS Telegram Mini Apps where custom CSS is avoided, system dark mode doesn't apply automatically to default HTML elements without specific meta tags.
**Action:** Always add `<meta name="color-scheme" content="light dark">` to the `<head>` to natively enable system dark mode support for default HTML elements in vanilla projects without custom CSS overhead.
