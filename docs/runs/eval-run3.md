# Step 33 eval — `run3` (`job-1791610584-955e05`)

**Release gate: FAIL**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (287/287) | ≥ 95% |
| evidence resolvability | 99.93% (15912/15923) | ≥ 90% |
| hallucinated paths | 6 of 900 checked | = 0 |
| hallucinated symbols (A9 functions) | 87 of 488 checked | = 0 |

## Agreement with golden labels (`evals/golden/corpus.json`)

| fact | agreement | misses |
|---|---|---|
| primary_language | 100.0% | — |
| framework | 66.67% | flask-tutorial (got None, want flask), musicstore (got None, want Microsoft.AspNetCore), sinatra (got None, want sinatra) |
| has_tests | 100.0% | — |
| has_data_layer | 90.0% | todomvc (got True, want False) |

## Variation with evidence

- P2 dispositions: {'Refactor': 10}
- P3 decomposition: 10 distinct boundary sets across 10 apps

## Unresolved evidence ids (sample)

- `{"artifact": "P1/flask-tutorial/A4", "id": "seed:A4-F1"}`
- `{"artifact": "P1/flask-tutorial/A4", "id": "seed:A4-F1"}`
- `{"artifact": "P1/flask-tutorial/A4", "id": "seed:A4-F1"}`
- `{"artifact": "P1/django-realworld-example-app/A4", "id": "seed:A4-F1"}`
- `{"artifact": "P1/django-realworld-example-app/A4", "id": "seed:A4-F1"}`
- `{"artifact": "P1/django-realworld-example-app/A4", "id": "seed:A4-F1"}`
- `{"artifact": "P1/musicstore/A4", "id": "seed:A4-F1"}`
- `{"artifact": "P1/musicstore/A4", "id": "seed:A4-F1"}`
- `{"artifact": "P1/musicstore/A4", "id": "seed:A4-F1"}`
- `{"artifact": "P1/sinatra/A4", "id": "seed:A4-F1"}`
- `{"artifact": "P1/sinatra/A4", "id": "seed:A4-F1"}`

## Hallucinated paths

- `{"artifact": "P1/flask-tutorial/A2", "path": "instance/flaskr.sqlite"}`
- `{"artifact": "P1/laravel58/A3", "path": "storage/logs/laravel.log"}`
- `{"artifact": "P1/laravel58/A3", "path": "database/database.sqlite"}`
- `{"artifact": "P1/sinatra/A2", "path": "topic/article.md"}`
- `{"artifact": "P1/sinatra/A9", "path": "topic/article.md"}`
- `{"artifact": "P1/golang-example/A2", "path": "A1/go.mod"}`

## Hallucinated symbols

- `{"artifact": "P1/spring-petclinic/A9", "symbol": "Visit constructor", "why": "not a code name"}`
- `{"artifact": "P1/node-express-realworld-example-app/A9", "symbol": "auth.controller.ts POST /users handler", "why": "not a code name"}`
- `{"artifact": "P1/musicstore/A9", "symbol": "StoreManagerController authorization", "why": "not a code name"}`
- `{"artifact": "P1/musicstore/A9", "symbol": "Album data annotations enforced by StoreManagerController.Create/Edit", "why": "not a code name"}`
- `{"artifact": "P1/musicstore/A9", "symbol": "StoreManagerController.Details/Create/Edit/RemoveAlbumConfirmed", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "GET / route closure", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "GET /user route closure", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "RegistersUsers trait", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "AuthenticatesUsers trait", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "SendsPasswordResetEmails trait", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "ResetsPasswords trait", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "VerifiesEmails trait", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "Broadcast::channel closure", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "Artisan::command closure", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "GET /user route closure", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "App\\User class configuration: $hidden", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "$fillable", "why": "not in source"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "$casts", "why": "not in source"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "inherited serialization/assignment methods", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "RedirectIfAuthenticated::handle($request", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "Closure $next", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "$guard = null)", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "consumed by framework password broker", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "Broadcast::channel closure", "why": "not a code name"}`
- `{"artifact": "P1/laravel58/A9", "symbol": "@auth and Route::has branches", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "get '/'", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "@@ layout", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "before '/p/:topic'", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "get '/p/:topic'", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "@@ layout", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "before '/p/:topic/:article'", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "get '/p/:topic/:article'", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "@@ layout", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "get '/activity'", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "@@ layout", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "get '/style.css'", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "@@ style", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "Not implemented in application methods", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "README 'How can I help?' and 'On translations'", "why": "not a code name"}`
- `{"artifact": "P1/sinatra/A9", "symbol": "app.rb @@ layout links to contribution guidance", "why": "not a code name"}`
