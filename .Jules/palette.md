## 2026-08-10 - Native Dark Mode in Vanilla Telegram Web Apps
**Learning:** In vanilla HTML/JS Telegram Mini Apps where custom CSS is avoided, we can natively enable system dark mode support for default HTML elements by using a `<meta name="color-scheme" content="light dark">` tag in the `<head>`. This prevents the flashing of white backgrounds on dark mode devices.
**Action:** Always add this meta tag to `index.html` in new vanilla Telegram Web Apps to ensure basic dark mode support without writing custom CSS.
