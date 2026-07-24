## 2024-03-20 - Native Dark Mode in Vanilla Web Apps
**Learning:** In vanilla Telegram Web Apps where custom CSS is avoided, we can easily enable native system dark mode support for default HTML elements using the `color-scheme` meta tag. This allows the browser to automatically adapt the background, text color, and basic default controls without needing manual CSS.
**Action:** Always include `<meta name="color-scheme" content="light dark">` in the HTML `<head>` for vanilla apps to ensure they align with the Telegram client's theme out-of-the-box.
