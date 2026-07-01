## 2024-05-24 - Avoid Viewport Scaling Restrictions
**Learning:** Adding `maximum-scale=1.0` or `user-scalable=no` to the viewport meta tag is an accessibility anti-pattern. While it might make an app feel more "native," it prevents mobile users with visual impairments from zooming in, directly violating WCAG guidelines.
**Action:** Never restrict user scaling in the viewport meta tag. Always allow users to zoom the interface as needed.
