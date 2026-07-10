## 2026-07-10 - Adding color-scheme to Telegram Mini Apps
**Learning:** Telegram Mini Apps default to a bright white flash when loading on dark mode clients if the `color-scheme` meta tag is missing, causing a poor initial experience.
**Action:** Always include `<meta name="color-scheme" content="light dark">` in the `<head>` of Telegram Mini Apps to ensure smooth transition to dark mode.