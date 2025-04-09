# frontend/Dockerfile
FROM node:20 as build

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy all files and build the app
COPY . .
RUN npm run build

# Use Nginx to serve the built frontend
FROM nginx:latest

# Copy build to Nginx HTML folder
COPY --from=build /app/dist /usr/share/nginx/html

# Copy Nginx configuration
COPY ./default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]