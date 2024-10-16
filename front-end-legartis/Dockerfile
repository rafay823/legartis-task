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
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app ./
EXPOSE 4200
CMD ["npm", "start"]