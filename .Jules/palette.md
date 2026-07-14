## 2024-05-24 - Add semantic layout and visual cues
**Learning:** Even simple Telegram Mini Apps benefit from semantic HTML landmarks (like `<main>`) for screen reader navigation. Furthermore, icon-only buttons or text-only buttons without clear visual distinction can reduce scannability.
**Action:** Always wrap primary content in a `<main>` tag for accessibility. Add visual cues (like an `aria-hidden` icon) to primary action buttons to improve scannability and affordance. Ensure buttons have an explicit `type="button"` to prevent unexpected form submission behavior.
