FROM node:20-alpine
WORKDIR /app
COPY package.json tsconfig.json next-env.d.ts next.config.js ./
COPY src ./src
RUN npm install
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0"]
