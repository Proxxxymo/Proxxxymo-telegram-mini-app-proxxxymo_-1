## 2024-05-14 - Telegram Mini App Native Feel
**Learning:** Telegram Mini Apps run in an environment where standard HTML UI can feel clunky (e.g. partial bottom sheets clipping content, lack of tactile feedback). Relying solely on web standard approaches misses native platform opportunities.
**Action:** When building Telegram Mini Apps, always use `Telegram.WebApp.expand()` upon load to claim the full viewport, and inject `Telegram.WebApp.HapticFeedback.impactOccurred('light')` into primary interactions like dismiss or submit buttons to create a native-feeling experience.
