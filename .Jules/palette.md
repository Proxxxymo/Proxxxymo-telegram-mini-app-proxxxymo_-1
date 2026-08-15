## 2024-03-22 - Native Dark Mode in Vanilla Web Apps
**Learning:** In vanilla HTML/JS projects where custom CSS is avoided, system dark mode support is missing by default which leads to blinding white flashes on load for dark mode users.
**Action:** Always add `<meta name="color-scheme" content="light dark">` to natively enable system dark mode support for default HTML elements in such projects.