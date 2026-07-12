## 2024-05-14 - Tactile Feedback in Telegram Mini Apps
**Learning:** Adding haptic feedback to primary actions like closing the app in Telegram Mini Apps significantly improves the tactile feel and confirms the interaction, making the app feel more native and responsive without artificial delays.
**Action:** Use `Telegram.WebApp.HapticFeedback.impactOccurred('light')` (or 'medium'/'heavy'/'rigid'/'soft') for immediate feedback on primary button clicks within TMA interfaces.
