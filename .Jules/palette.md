## 2026-09-21 - Native System Dark Mode Support
**Learning:** In vanilla Telegram Web Apps where custom CSS is avoided, default HTML elements don't automatically adapt to the user's system dark mode setting, leading to jarring UX when opened in a dark-themed app.
**Action:** Always include `<meta name="color-scheme" content="light dark">` in the HTML head to natively enable system dark mode support for default HTML elements without needing extra CSS.
