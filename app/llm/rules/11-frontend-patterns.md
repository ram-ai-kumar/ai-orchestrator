---
name: Enterprise Frontend Policy
description: Rules for React/TypeScript and Flutter/Dart at scale.
---

# Frontend & Client Policy (2026 Standard)

## 1. Type Safety & Validation

- **Strict Mode**: `strict: true` for all TS projects. No `any` types permitted without a documented waiver and an explicit `todo` for refactoring.
- **Runtime Validation**: Use `zod` for all API-to-Client data boundary validations. Trusting the server's contract at the edge is a security vulnerability.

## 2. Architecture & State

- **State Sovereignty**: Prefer server-state (React Query/SWR) over client-side global stores (Redux/Zustand) for fetched data.
- **Component Design**:
  - Keep components under 200 lines.
  - Business logic must reside in Hooks/Services, never in the UI layer.
  - Props must be optimized for memoization; avoid passing object literals that trigger re-renders.

## 3. UX & Performance

- **Accessibility**: All UI components must be WCAG 2.2 compliant. Use semantic HTML and `aria` roles.
- **Core Web Vitals**: LCP (Largest Contentful Paint) must be < 2.5s. Code-splitting must be implemented for all routes.
- **Flutter**: Use `const` constructors for all static widgets to maximize UI tree rebuild performance.
