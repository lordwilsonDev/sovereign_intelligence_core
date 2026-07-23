# Sovereign Stack — PocketBase/Go/HTMX Reference Architecture

**Status:** Reference only — not incorporated into `msb-v2` unless explicitly requested later.

---

## 1. Directory Structure

```text
/sovereign-stack
  ├── main.go
  ├── go.mod
  ├── go.sum
  └── /views
      ├── layout.html
      └── fragment.html
```

## 2. HTML Templates

**`views/layout.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sovereign Node Interface</title>
  <script src="https://unpkg.com/htmx.org@1.9.10"></script>
</head>
<body>
  <h1>System Console</h1>
  <form hx-post="/api/custom/execute" hx-target="#output-log" hx-swap="beforeend">
    <input type="text" name="command" placeholder="Enter command..." required>
    <button type="submit">Execute</button>
  </form>
  <div id="output-log"></div>
</body>
</html>
```

**`views/fragment.html`**
```html
<div class="log-entry">
  <strong>Execution logged:</strong> {{.Command}} 
  <span style="color: gray;">(Status: {{.Status}})</span>
</div>
```

## 3. Go Backend

```go
package main

import (
	"embed"
	"html/template"
	"log"
	"net/http"
	"strings"

	"github.com/pocketbase/pocketbase"
	"github.com/pocketbase/pocketbase/apis"
	"github.com/pocketbase/pocketbase/core"
)

//go:embed views/*
var views embed.FS

func main() {
	app := pocketbase.New()
	tmpl, err := template.ParseFS(views, "views/*.html")
	if err != nil {
		log.Fatal("Failed to parse templates:", err)
	}
	app.OnBeforeServe().Add(func(e *core.ServeEvent) error {
		e.Router.GET("/console", func(c echo.Context) error {
			return c.HTMLBlob(http.StatusOK, renderTemplate(tmpl, "layout.html", nil))
		})
		e.Router.POST("/api/custom/execute", func(c echo.Context) error {
			command := c.FormValue("command")
			data := map[string]string{"Command": command, "Status": "Success"}
			return c.HTMLBlob(http.StatusOK, renderTemplate(tmpl, "fragment.html", data))
		})
		return nil
	})
	if err := app.Start(); err != nil {
		log.Fatal(err)
	}
}

func renderTemplate(tmpl *template.Template, name string, data map[string]string) []byte {
	var buf strings.Builder
	err := tmpl.ExecuteTemplate(&buf, name, data)
	if err != nil {
		log.Println("Template rendering error:", err)
		return []byte("Error rendering template")
	}
	return []byte(buf.String())
}
```

## 4. Notes

- Goal: single sovereign binary, no external dependencies.
- Uses Go `embed` to bake `views/` into the executable.
- Frontend: HTMX for dynamic partial updates.
- Framework: PocketBase replaces the pre-compiled executable.
- Next action if activated: `go mod init sovereign-stack && go mod tidy && go build`.
