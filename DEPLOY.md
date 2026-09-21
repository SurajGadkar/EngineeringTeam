# Deployment — Engineering Team (Iteration 1)

## Build
```bash
# Server
cd workspace/app/server && npm install && node index.js
# Client (requires vite build)
cd ../client && npm install && npm run build
```

## Docker Compose (isolated)
```bash
docker-compose up --build
```
- MongoDB on 27017
- Server on 5000 (AI proxy /api/ai/chat with openRouter/free)
- Client static build served via nginx or `vite preview`

## Production Notes
- Set OPENROUTER_API_KEY in .env (or through env manager)
- JWT_SECRET must be rotated in production
- Use HTTPS; restrict CORS to your domain
- Monitor AI endpoint latency (<5s target)

## AI Integration
- Endpoint: POST /api/ai/chat
- Model: openai/gpt-3.5-turbo via OpenRouter/free
- No client-side keys exposed (proxy pattern)
