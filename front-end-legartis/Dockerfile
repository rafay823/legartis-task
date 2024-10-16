# Use Node.js image for building the Angular app
FROM node:18-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire application code
COPY . .

# Build the Angular application
RUN npm run build --prod

# Use Nginx to serve the application
FROM nginx:latest

# Copy the built files from the builder stage
COPY --from=builder /app/dist/project /usr/share/nginx/html

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose the port Nginx will run on
EXPOSE 80

# Command to run Nginx
CMD ["nginx", "-g", "daemon off;"]
