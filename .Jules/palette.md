## 2024-06-25 - Enabling dark mode in vanilla Telegram Web Apps
**Learning:** Telegram Web Apps follow system-level color schemes, but vanilla HTML fails to properly apply the system's dark theme to default elements (like the background and text color) without explicit instruction.
**Action:** Always include `<meta name="color-scheme" content="light dark">` in the HTML head when building vanilla Web Apps to seamlessly inherit Telegram's native dark mode settings.
