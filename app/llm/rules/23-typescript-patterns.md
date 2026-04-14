---
name: TypeScript Patterns
description: Language-specific best practices for TypeScript/Node.js projects (React, Next.js, NestJS, standalone APIs) — enforced by audit-code-quality and verify-code-quality.
alwaysApply: false
---

# TypeScript Patterns

Detected via: `package.json`, `tsconfig.json`, `tsconfig.*.json`, `.eslintrc.*`, `next.config.*`, `nest-cli.json`

## 1. TypeScript Configuration

1. **`strict: true` is non-negotiable**: `tsconfig.json` must have `"strict": true`. This enables `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, and more.
2. **Additional strict flags required**:
   ```json
   {
     "noUncheckedIndexedAccess": true,
     "exactOptionalPropertyTypes": true,
     "noImplicitReturns": true,
     "noFallthroughCasesInSwitch": true
   }
   ```
3. **No `any`**: Use `unknown` and narrow with type guards. If `any` is unavoidable, mark with `// eslint-disable-next-line @typescript-eslint/no-explicit-any` and a justification comment.
4. **No `as` casting without validation**: Type assertions bypass the type system. Only cast after runtime validation (e.g., via Zod `parse()`).
5. **No `!` non-null assertion**: Handle `null`/`undefined` explicitly. Every `!` is a runtime crash waiting to happen.

## 2. ESLint & Formatting

1. **ESLint with `@typescript-eslint`**: Extend `plugin:@typescript-eslint/strict-type-checked`. Zero warnings tolerated in CI.
2. **Prettier for formatting**: `prettier --check` in CI. No manual style debates.
3. **Import ordering**: Use `eslint-plugin-import` with `import/order` rule. Enforce: built-in → external → internal → relative.
4. **`eslint-plugin-security`**: Enabled. Catches `eval`, prototype pollution, and regex ReDoS risks.

## 3. Runtime Validation (the `any`-killer)

1. **Zod at every external boundary**: API request bodies, environment variables, API responses from 3rd parties, message queue payloads — all parsed with Zod `schema.parse()` before use.
2. **Env vars via `zod` + a typed config module**:
   ```typescript
   const envSchema = z.object({
     DATABASE_URL: z.string().url(),
     JWT_SECRET: z.string().min(32),
   });
   export const env = envSchema.parse(process.env);
   ```
3. **Never trust `JSON.parse()`**: Always wrap in `schema.safeParse()` and handle the error case.

## 4. Async & Error Handling

1. **Async/await over raw Promises**: No `.then().catch()` chains. Use `async/await` with `try/catch`.
2. **No floating Promises**: Every `Promise` must be `await`ed or explicitly `.catch()`-handled. Enable `@typescript-eslint/no-floating-promises` as an error.
3. **Typed error handling**:
   ```typescript
   // Prefer Result types over throwing for known failure paths
   type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
   ```
4. **`finally` for resource cleanup**: DB connections, file handles, locks — always released in `finally`.
5. **Structured logging**: Use `pino` or `winston` with JSON format. Every log must include `requestId`, `tenantId`, and relevant entity IDs. Never log PII.

## 5. NestJS Patterns

1. **Module boundaries**: Each domain is a NestJS module. Cross-domain access only via exported services, never by importing another module's repository directly.
2. **DTOs with `class-validator`**: Every controller input is a DTO class with `@IsString()`, `@IsEmail()`, etc. Enable `ValidationPipe` globally with `whitelist: true, forbidNonWhitelisted: true`.
3. **Guards for auth/authz**: `JwtAuthGuard` and `RolesGuard` applied globally. Per-route overrides with `@Public()` or `@Roles()` decorators.
4. **Interceptors for cross-cutting concerns**: Logging, response transformation, timing — via `NestInterceptor`. Never in controllers.
5. **Tenant scoping in repositories**: Every repository method must accept `tenantId` or read it from a request-scoped `TenantContext`. Never query without tenant scope.

## 6. React / Next.js Patterns

1. **Server Components by default** (Next.js App Router): Only add `'use client'` when the component genuinely needs browser APIs or React state.
2. **No `useEffect` for data fetching**: Use React Query (`@tanstack/query`), SWR, or Next.js `fetch` with caching. `useEffect` for data is an anti-pattern.
3. **No prop drilling beyond 2 levels**: Use React Context or a state management library (Zustand, Jotai). Document the context's purpose clearly.
4. **Accessible by default**: Every interactive element must have an accessible label. Run `eslint-plugin-jsx-a11y`. No ARIA attributes without understanding their semantics.
5. **Environment variables**: Public vars use `NEXT_PUBLIC_` prefix. Secret vars are never exposed to the client bundle. Validate both sets with Zod at startup.
6. **No `dangerouslySetInnerHTML`**: If unavoidable, sanitize input with `DOMPurify` first. Flag every use for security review.

## 7. API Design (REST)

1. **Versioned routes**: `/api/v1/`. No unversioned API endpoints.
2. **Consistent response envelope**:
   ```typescript
   type ApiResponse<T> = {
     data: T;
     meta?: { page: number; total: number };
     errors?: Array<{ field: string; message: string }>;
   };
   ```
3. **HTTP status discipline**: `200` OK, `201` Created, `400` Bad Request, `401` Unauthenticated, `403` Forbidden, `404` Not Found, `409` Conflict, `422` Validation Error, `429` Rate Limited.
4. **Idempotency keys**: State-changing `POST` endpoints (payments, orders) must accept `Idempotency-Key` header and return the same response for duplicate requests.
5. **Rate limiting**: Apply per-user, per-tenant rate limits. Use `@nestjs/throttler` or equivalent. Return `Retry-After` header on 429.

## 8. Security

1. **CORS**: Explicit allowlist only. Never `origin: '*'` in production.
2. **Helmet**: Enable `helmet()` middleware in every Express/NestJS app. Includes CSP, HSTS, X-Frame-Options.
3. **JWT**: Short-lived access tokens (15 min). Refresh tokens stored in httpOnly, Secure, SameSite=Strict cookies — never in `localStorage`.
4. **Input sanitization**: Sanitize all string inputs before storing. Use `DOMPurify` for HTML, `validator.js` for structured formats.
5. **`npm audit`**: Run in CI. Zero high/critical CVEs. Use `overrides` in `package.json` only as a documented temporary fix.
6. **Dependency pinning**: Exact versions in `package.json` for production dependencies. `package-lock.json` committed and used with `npm ci` in CI.

## 9. Testing

1. **Vitest or Jest with `ts-jest`**: No test transpilation shortcuts. Full type checking in tests.
2. **Testing pyramid**: Unit (services, utilities) > Integration (API routes) > E2E (critical paths). 70/20/10 ratio target.
3. **MSW for API mocking**: Use `msw` (Mock Service Worker) for external HTTP dependency mocking. Consistent between tests and browser dev.
4. **`@testing-library/react`**: User-event based testing. No direct DOM manipulation. Test behavior, not implementation.
5. **Coverage gate**: 80% line coverage minimum in CI. Exclude generated files and `*.d.ts`.
6. **Negative tests**: Every endpoint tested for 401, 403, and 422 cases. Every Zod schema tested with invalid inputs.
