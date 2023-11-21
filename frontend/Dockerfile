FROM node:lts AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG FORM_ACTION
ENV FORM_ACTION=$FORM_ACTION
RUN npm run build

FROM nginx:alpine AS runtime
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080