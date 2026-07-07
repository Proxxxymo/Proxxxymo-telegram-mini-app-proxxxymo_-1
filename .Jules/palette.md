## 2024-07-07 - Instant Feedback without Delays
**Learning:** Adding artificial delays (e.g., `setTimeout`) to UI actions like closing an app just to show a state change is a UX anti-pattern. It makes the application feel sluggish.
**Action:** Always provide immediate visual/tactile feedback (e.g., disabling a button, changing text, setting `aria-busy`) right before instantaneously executing the action to ensure the application remains responsive and fast.
