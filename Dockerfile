# Multi-stage build of the pinned vue tree - a realistic CI docker workload.
FROM node:20-slim AS build
WORKDIR /app
COPY vue/ .
RUN corepack enable && pnpm install --frozen-lockfile && pnpm build
FROM node:20-slim
COPY --from=build /app/packages/vue/dist /dist
CMD ["node", "-e", "console.log('ok')"]
