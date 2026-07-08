
## 2023-10-27 - [Telegram Mini Apps and Keyboard Modals]
**Learning:** Telegram Mini Apps do not inherently handle modal-like keyboard interactions out of the box (e.g., using 'Escape' to close the app). This means desktop users or screen reader users relying on keyboard shortcuts can get trapped or have poor UX when trying to exit the app.
**Action:** When working with Telegram Mini Apps, explicitly bind the 'Escape' key to `Telegram.WebApp.close()` and use `aria-keyshortcuts` on close buttons to ensure full keyboard accessibility.
