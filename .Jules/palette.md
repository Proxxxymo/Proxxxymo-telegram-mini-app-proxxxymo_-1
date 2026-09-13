## 2026-09-13 - System Dark Mode Support
**Learning:** In vanilla Telegram Web Apps where custom CSS is avoided, using `<meta name="color-scheme" content="light dark">` in the HTML head natively enables system dark mode support for default HTML elements.
**Action:** Always add this meta tag to simple Telegram Mini Apps to respect the user's system theme preferences without needing complex CSS.
