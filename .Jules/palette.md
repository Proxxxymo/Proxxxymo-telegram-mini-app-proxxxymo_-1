## 2026-08-21 - Native dark mode support in vanilla Telegram Web Apps
**Learning:** In vanilla Telegram Web Apps where custom CSS is avoided, using `<meta name="color-scheme" content="light dark">` in the HTML head natively enables system dark mode support for default HTML elements without needing extra CSS.
**Action:** Always add this meta tag to `index.html` in vanilla apps to respect user's system preferences for dark mode natively.
