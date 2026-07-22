## 2024-05-24 - Context-Rich ARIA Labels for Mini Apps
**Learning:** Screen reader users interacting with generic action buttons (like "Закрыть" / "Close") in embedded contexts (like Telegram Mini Apps) often lose context of what they are closing if the app's title is not consistently read or if focus is lost. A simple "Close" label can be ambiguous.
**Action:** Always enrich generic action buttons with app-specific context in their `aria-label` (e.g., "Закрыть мини-приложение") to provide clear boundaries and expectations for assistive technologies.
