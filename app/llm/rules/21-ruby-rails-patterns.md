---
name: Ruby / Rails Patterns
description: Language-specific best practices for Ruby and Ruby on Rails projects — enforced by audit-code-quality and verify-code-quality.
alwaysApply: false
---

# Ruby / Rails Patterns

Detected via: `Gemfile`, `Gemfile.lock`, `.ruby-version`, `config/application.rb`

## 1. Code Style & Linting

1. **RuboCop enforced**: All files must pass `rubocop --format json` with zero offenses at the agreed config. Never disable cops inline (`# rubocop:disable`) without a documented reason in the same comment.
2. **Line length**: Max 120 characters. Long method chains must be broken with trailing `.` on each line.
3. **Frozen string literals**: Every file must begin with `# frozen_string_literal: true` to prevent accidental mutation and reduce GC pressure.
4. **No `attr_accessor` for write-only or read-only fields**: Use `attr_reader` or `attr_writer` specifically.
5. **Guard clauses over nested conditionals**: Return early rather than deeply nesting `if/else` blocks.

## 2. Rails-Specific Patterns

### Models
1. **Thin models**: Models must not contain business logic beyond validations, associations, and scopes. Extract to service objects or query objects.
2. **Validations**: All user-facing attributes must have explicit `validates` declarations. Never rely solely on DB constraints for user-visible feedback.
3. **Scopes over class methods** for chainable queries. Scopes must return `ActiveRecord::Relation` (use `-> { }` lambda form).
4. **No `default_scope`**: It creates invisible, hard-to-debug query side effects. Be explicit.
5. **Callbacks only for model-internal concerns**: Never trigger external service calls (email, webhooks, APIs) in `before_save`, `after_create`, etc. Use explicit service objects instead.
6. **Tenant isolation**: Every query involving user data must scope by `tenant_id`. Never query across tenants.
   ```ruby
   # BAD
   User.where(email: email)
   # GOOD
   current_tenant.users.where(email: email)
   ```

### Controllers
1. **Fat-free controllers**: Controllers must only authenticate, authorize, call one service object, and render. Max ~10 lines of logic per action.
2. **`before_action` for authentication and authorization**: Use Pundit or CanCanCan. Never inline `if current_user.admin?` in action bodies.
3. **Strong parameters always**: Every `params` usage must go through explicit `permit()`. No `params.permit!`.
4. **Rescue at the boundary**: Use `rescue_from` in `ApplicationController` for known error classes. Never let raw exceptions reach the user.

### Services & Query Objects
1. **One public method per service object**: `call` or `execute`. Keep the interface predictable.
2. **Return value discipline**: Services must return a consistent result object (e.g., `ServiceResult`) with `success?`, `errors`, and `value`. Never return `nil` for failure.
3. **Query objects**: All complex queries (joins, subqueries, window functions) must live in a dedicated query object under `app/queries/`.

## 3. Security

1. **Mass assignment protection**: `permit` only explicitly listed attributes. Never permit `:id`, `:admin`, `:tenant_id` from user input.
2. **SQL injection**: Always use parameterized queries. Never interpolate user input into `where` strings.
   ```ruby
   # BAD — SQL injection
   User.where("email = '#{params[:email]}'")
   # GOOD
   User.where(email: params[:email])
   ```
3. **IDOR prevention**: Always scope queries to the authenticated tenant/user. Use Pundit policy scope as the default filter.
4. **Secret management**: No credentials in `config/database.yml`, `config/secrets.yml`, or any committed file. Use `Rails.application.credentials` backed by environment-specific keys stored in a vault.
5. **`brakeman` scan**: Run `brakeman --no-pager -q` on every CI run. Zero warnings tolerance for High/Critical severity.

## 4. Performance

1. **N+1 queries**: Use `includes`, `preload`, or `eager_load`. Run `bullet` gem in development and treat all N+1 warnings as errors in CI.
2. **Background jobs for all non-trivial work**: Email sends, webhooks, report generation, and data exports must go through Sidekiq (or equivalent). Never block a controller response.
3. **Database indexes**: Every `belongs_to` foreign key, every `where`-filtered column, and every `order`-by column must have a database index.
4. **Pagination**: Never return unbounded `all` collections via API. Use `kaminari` or `pagy`. Default page size ≤ 100.
5. **Counter caches**: Use Rails counter cache for `count` queries on associations accessed frequently.

## 5. Testing (RSpec)

1. **Testing pyramid**: Unit (service objects, models) > Integration (request specs) > System (Capybara). Aim for 70/20/10 ratio.
2. **Factory Bot only**: No fixtures. Factories must use `sequence` for unique fields.
3. **No `let` over-use**: Prefer explicit local variables in `it` blocks for clarity. Use `let` only for shared expensive setup.
4. **Request specs over controller specs**: Test APIs via `rails_helper` request specs with full HTTP stack.
5. **Negative tests mandatory**: Every API endpoint must have a spec for unauthorized access (401/403) and invalid input (422).
6. **VCR or WebMock for external calls**: Never make real HTTP requests in tests. Record cassettes in CI.

## 6. API Design (Rails API mode)

1. **Versioned routes**: All APIs must be under `/api/v1/`. No unversioned endpoints.
2. **JSON:API or consistent envelope**: Standardize response shape across all endpoints. Use `{ data: {}, meta: {}, errors: [] }`.
3. **HTTP status codes**: `200` for success, `201` for created, `422` for validation errors, `401` for unauthenticated, `403` for unauthorized, `404` for not found. Never return `200` with an error body.
4. **Idempotency keys**: All `POST` endpoints that trigger financial or state-changing operations must accept and honor `Idempotency-Key` headers.

## 7. Dependency Management

1. **Gemfile.lock committed**: Always committed. CI must use `bundle install --frozen`.
2. **No unpinned major versions**: Pin gems with `~>` to minor version. Review updates intentionally.
3. **`bundler-audit`**: Run `bundle audit check --update` in CI. Zero known CVEs tolerated.
4. **Minimize gem count**: Evaluate every new gem addition. Prefer stdlib or a small focused gem over a large framework gem.
