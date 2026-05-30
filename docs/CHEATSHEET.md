# TestForge — Visual Summary Cheat Sheet

## 🎯 At a Glance

**TestForge** = E2E + API Testing Platform
- ✅ Tests GitHub.com website (real browser)
- ✅ Tests api.github.com REST endpoints
- ✅ Generates beautiful HTML report
- ✅ Runs automatically on every GitHub commit
- ✅ Designed to be reusable for ANY web app/API

## 🚀 Quick Start (3 commands)

```bash
cd testforge
make install
make test-all
```

View report: `open reports/combined-test-report.html`

## 📊 What You'll See

- **70 Tests** (30 E2E + 40 API)
- **100% Pass Rate** (when working)
- **3-4 minutes** execution time
- **Beautiful dashboard** with metrics

## ⚡ Command Shortcuts

```bash
make install              # Setup dependencies
make test-all             # Run everything
make test-e2e             # E2E only
make test-api             # API only
make report               # Generate report
make clean                # Clean artifacts
```

## 🌐 Tech Stack

| Layer | Tool | Language |
|-------|------|----------|
| E2E | Playwright | TypeScript |
| API | pytest | Python |
| Report | HTML + CSS | Self-contained |

## 📁 Key Files

```
testforge/
├── e2e/tests/           ← E2E test files
├── api/tests/           ← API test files
├── reports/             ← Generated reports
├── Makefile             ← Commands
└── package.json/requirements.txt
```

## ✅ You're Ready!

Run `make test-all` and open the HTML report in your browser. 🎉
