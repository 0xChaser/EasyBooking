FROM node:23

WORKDIR /app

COPY package.json package-lock.json* ./

RUN rm -f package-lock.json && \
    npm install && \
    npm install lightningcss --force

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]