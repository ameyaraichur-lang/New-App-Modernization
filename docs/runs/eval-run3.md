# Step 33 eval — `run3` (`job-1791610584-955e05`)

**Release gate: FAIL**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (287/287) | ≥ 95% |
| evidence resolvability | 99.93% (15912/15923) | ≥ 90% |
| hallucinated paths | 3 of 900 checked | = 0 |
| hallucinated symbols (A9 functions) | 80 of 488 checked | = 0 |

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

- `{"artifact": "P1/sinatra/A2", "path": "topic/article.md"}`
- `{"artifact": "P1/sinatra/A9", "path": "topic/article.md"}`
- `{"artifact": "P1/golang-example/A2", "path": "A1/go.mod"}`

## Hallucinated symbols

- `{"artifact": "P1/spring-petclinic/A9", "problem": "business_rules: function 'Visit constructor' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/node-express-realworld-example-app/A9", "problem": "business_rules: function 'auth.controller.ts POST /users handler' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/musicstore/A9", "problem": "business_rules: function 'StoreManagerController authorization' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/musicstore/A9", "problem": "business_rules: function 'Album data annotations enforced by StoreManagerController.Create/Edit' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/musicstore/A9", "problem": "business_rules: function 'StoreManagerController.Details/Create/Edit/RemoveAlbumConfirmed' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "processes: function 'GET / route closure' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "processes: function 'GET /user route closure' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "processes: function 'RegistersUsers trait' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "processes: function 'AuthenticatesUsers trait' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "processes: function 'SendsPasswordResetEmails trait' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "processes: function 'ResetsPasswords trait' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "processes: function 'VerifiesEmails trait' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "business_rules: function 'GET /user route closure' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "business_rules: function 'App\\\\User class configuration: $hidden' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "business_rules: function 'inherited serialization/assignment methods' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "business_rules: function 'Closure $next' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "business_rules: function '$guard = null)' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/laravel58/A9", "problem": "business_rules: function 'consumed by framework password broker' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function \"get '/'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function '@@ layout' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function \"before '/p/:topic'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function \"get '/p/:topic'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function '@@ layout' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function \"before '/p/:topic/:article'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function \"get '/p/:topic/:article'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function '@@ layout' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function \"get '/activity'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function '@@ layout' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function \"get '/style.css'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function '@@ style' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function 'Not implemented in application methods' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function \"README 'How can I help?' and 'On translations'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "processes: function 'app.rb @@ layout links to contribution guidance' is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "business_rules: function \"get '/p/:topic'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "business_rules: function \"get '/p/:topic/:article'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "business_rules: function \"get '/p/:topic'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "business_rules: function \"get '/p/:topic/:article'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "business_rules: function \"get '/activity'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "business_rules: function \"get '/p/:topic'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
- `{"artifact": "P1/sinatra/A9", "problem": "business_rules: function \"get '/p/:topic/:article'\" is not a declared code name \u2014 list exact names only, or '' for an anonymous handler"}`
