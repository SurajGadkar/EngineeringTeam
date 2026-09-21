# Engineering Plan — MERN + AI

## Prompt
Minimalist Kanban Task Board (Trello Lite): single-page React dashboard with three columns (To Do, In Progress, Done), MongoDB persistence, full CRUD API, add/move/delete tasks

## Vision
AI-powered web application with user auth, CRUD, and an openRouter/free AI chatbot.

## Architecture
- MongoDB via Mongoose (users, tasks, messages collections)
- Express REST API (auth, tasks, ai/chat endpoints)
- React (Vite) SPA with AI chat widget
- OpenRouter/free: `openai/gpt-3.5-turbo` via server proxy (no key exposure)

## Additional Tech
- `express`, `mongoose`, `cors`, `bcryptjs`, `jsonwebtoken`
- Client: `react`, `axios`, `react-router-dom`
- Tests: `vitest` (client), `jest`/`supertest` (server)
- Docker for deployment

## Milestones (max 5 iterations)
1. Plan / Setup
2. Backend + DB + AI proxy
3. Frontend + AI widget
4. Tests + QA review
5. Deploy / Signoff

## QA Criteria
- All backend + frontend tests pass (>=95%)
- AI endpoint responds within 5s
- Responsive design
- Security (no exposed keys, hashed passwords, CORS restricted)
