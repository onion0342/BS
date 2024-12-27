FROM node:18-alpine

WORKDIR /app

RUN npm config set registry https://registry.npmmirror.com

COPY package*.json ./
RUN npm install --retry=3 --timeout=60000

COPY . .

RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"] 