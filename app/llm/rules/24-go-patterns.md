---
name: Go Patterns
description: Language-specific best practices for Go services and CLIs — enforced by audit-code-quality and verify-code-quality.
alwaysApply: false
---

# Go Patterns

Detected via: `go.mod`, `go.sum`, `main.go`, `Makefile` with `go build`

## 1. Code Style & Tooling

1. **`gofmt` / `goimports`**: All code must be formatted. CI fails if `gofmt -l .` outputs any files. Use `goimports` to manage imports automatically.
2. **`golangci-lint`**: Run with a strict config (`golangci-lint run`). Required linters: `errcheck`, `govet`, `staticcheck`, `gosec`, `revive`, `exhaustive`, `gocyclo`. Zero warnings in CI.
3. **`staticcheck`**: Run independently. Catches deprecated API usage, unreachable code, and incorrect format strings.
4. **Naming**: Follow standard Go conventions — `CamelCase` for exported, `camelCase` for unexported. No underscores except in test file names (`_test.go`) and generated code.
5. **Package naming**: Short, lowercase, single-word. No `utils`, `helpers`, `common` — name by domain (`auth`, `billing`, `tenant`).

## 2. Error Handling

1. **Never ignore errors**: Every function returning an `error` must have its error checked. `_ = someFunc()` is prohibited unless the function is documented as error-free.
   ```go
   // BAD
   file, _ := os.Open(path)
   // GOOD
   file, err := os.Open(path)
   if err != nil {
       return fmt.Errorf("open config %s: %w", path, err)
   }
   ```
2. **Wrap errors with context**: Use `fmt.Errorf("operation context: %w", err)` at every layer. This preserves the chain for `errors.Is()` and `errors.As()`.
3. **Sentinel errors for known failure modes**: Define `var ErrNotFound = errors.New("not found")` for errors callers need to check. Never return raw strings.
4. **Custom error types for structured errors**: Implement `error` interface for errors carrying additional data (e.g., validation errors with field names).
5. **`panic` is prohibited** in production code paths. Only acceptable in `init()` for configuration that is fundamentally broken. Recover at the outermost HTTP handler.

## 3. Project Structure

```
cmd/
  myservice/
    main.go          ← thin: parse flags, wire dependencies, call app.Run()
internal/
  auth/
  billing/
  tenant/
  platform/
    db/
    cache/
    observability/
pkg/                 ← shared across multiple cmd/ binaries only
  apierrors/
  pagination/
api/                 ← protobuf, OpenAPI specs
migrations/
```

1. **`internal/` for domain logic**: Never expose internal packages to external consumers.
2. **`cmd/` for entrypoints only**: `main.go` must only wire dependencies and start the server. Business logic belongs in `internal/`.
3. **Dependency injection via constructor functions**: `NewUserService(db *sql.DB, cache *redis.Client) *UserService`. No global variables for dependencies.
4. **Interface-driven design**: Define small, purpose-specific interfaces at the point of use (consumer side). Never define large "god interfaces".
   ```go
   // Define where it's used, not where it's implemented
   type UserStore interface {
       FindByID(ctx context.Context, id uuid.UUID) (*User, error)
   }
   ```

## 4. Context

1. **`context.Context` as first parameter always**: Every function doing I/O, calling external services, or performing long operations must accept `ctx context.Context` as the first parameter.
2. **Never store context in structs**: Pass it through the call chain. Storing in structs breaks cancellation propagation.
3. **Check cancellation in loops**: Long-running loops must check `ctx.Done()`.
   ```go
   for {
       select {
       case <-ctx.Done():
           return ctx.Err()
       case item := <-ch:
           process(item)
       }
   }
   ```
4. **Context values for request-scoped metadata only**: `trace_id`, `tenant_id`, `request_id`. Never use context for passing optional parameters — use function arguments.

## 5. Concurrency

1. **`sync.WaitGroup` for goroutine lifecycle**: Always track goroutines. Never fire-and-forget without a cleanup mechanism.
2. **Channel ownership**: The goroutine that creates a channel is responsible for closing it. Document ownership in comments.
3. **`errgroup` for concurrent work with error collection**: Use `golang.org/x/sync/errgroup` instead of raw goroutine + channel for fan-out patterns.
4. **No data races**: Run `go test -race ./...` in CI. Zero race conditions tolerated.
5. **Mutexes**: Prefer `sync.RWMutex` for read-heavy shared state. Lock the smallest critical section possible. Document which mutex protects which fields.

## 6. Database

1. **`database/sql` with `pgx` driver**: Use `pgx/v5` for PostgreSQL. Never `lib/pq` (deprecated for new projects).
2. **Connection pool configuration**: Always set `MaxOpenConns`, `MaxIdleConns`, `ConnMaxLifetime`, `ConnMaxIdleTime`. Never use default unbounded pool.
3. **Parameterized queries always**: Never concatenate user input into SQL strings.
   ```go
   // BAD — SQL injection
   db.Query("SELECT * FROM users WHERE email = '" + email + "'")
   // GOOD
   db.QueryContext(ctx, "SELECT * FROM users WHERE email = $1", email)
   ```
4. **Tenant isolation**: Every query must include `WHERE tenant_id = $1`. Use a repository pattern that enforces this at the type level.
5. **Transactions**: Use `db.BeginTx(ctx, nil)` with explicit `defer tx.Rollback()` and `tx.Commit()` only on success.
6. **Migrations via `golang-migrate`**: Never `ALTER TABLE` manually in production. All schema changes via versioned migration files.

## 7. HTTP Services

1. **`net/http` + a minimal router** (`chi`, `gorilla/mux`): No full-framework lock-in unless the team has committed to it.
2. **Graceful shutdown**: Always handle `SIGTERM`/`SIGINT` with a shutdown context and `server.Shutdown(ctx)`.
   ```go
   quit := make(chan os.Signal, 1)
   signal.Notify(quit, syscall.SIGTERM, syscall.SIGINT)
   <-quit
   ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
   defer cancel()
   server.Shutdown(ctx)
   ```
3. **Middleware for cross-cutting concerns**: Request ID injection, structured logging, panic recovery, auth — all via middleware. Never in handlers.
4. **Timeouts on all outgoing requests**: Every `http.Client` must have `Timeout` set. Never use `http.DefaultClient` in production.
5. **Response encoding**: Always return `Content-Type: application/json`. Use `json.NewEncoder(w).Encode(resp)` — avoid `json.Marshal` + `w.Write` for large responses (avoids buffering).

## 8. Security

1. **`gosec`**: Run `gosec ./...` in CI. Zero G1xx (injection), G2xx (crypto), G4xx (auth) issues tolerated.
2. **No `math/rand` for security-sensitive operations**: Always use `crypto/rand`.
3. **TLS config**: Never use `InsecureSkipVerify: true`. Configure minimum TLS 1.2 (prefer 1.3). Explicit cipher suites.
4. **Secret injection via environment only**: Read secrets from `os.Getenv()` through a validated config struct at startup. Never from files committed to the repo.
5. **Input size limits**: All HTTP request bodies must have `http.MaxBytesReader(w, r.Body, maxBytes)` applied before reading.

## 9. Observability

1. **OpenTelemetry**: Instrument with `go.opentelemetry.io/otel`. Every service entry point starts a span. Propagate trace context via HTTP headers.
2. **Structured logging with `slog`** (Go 1.21+): `slog.InfoContext(ctx, "message", "key", value)`. Every log entry must carry `trace_id`, `tenant_id`, `request_id`.
3. **Prometheus metrics**: Instrument request count, latency (histogram), and error rate for every HTTP handler and background worker.
4. **Health endpoints**: `/health/live` (process alive) and `/health/ready` (dependencies reachable). Both must check actual dependency connectivity, not just return 200.

## 10. Testing

1. **Table-driven tests**: Standard Go pattern for unit tests with multiple input/output cases.
2. **`testify/require` for assertions**: `require.NoError(t, err)` fails fast. `assert` continues — use deliberately.
3. **`go test -race -cover ./...`**: Both race detector and coverage in CI. 80% coverage minimum.
4. **Test doubles via interfaces**: Mock by satisfying the interface. Use `github.com/stretchr/testify/mock` or hand-written fakes.
5. **Integration tests with `testcontainers-go`**: Spin up real Postgres/Redis containers for integration tests. Never mock the DB layer in integration tests.
6. **Negative tests**: Every handler must have tests for unauthenticated, forbidden, invalid input, and missing resource scenarios.

## 11. Module Management

1. **`go mod tidy`** must leave no diff in CI. Automated check: `go mod tidy && git diff --exit-code go.sum`.
2. **`govulncheck`**: Run `govulncheck ./...` in CI. Zero known vulnerabilities.
3. **Minimal dependencies**: Go's stdlib is extensive. Prefer it over third-party packages. Every new dependency requires justification.
4. **Pin indirect dependencies**: Review `go.sum` changes in PRs — unexplained new indirect deps are a supply-chain risk.
