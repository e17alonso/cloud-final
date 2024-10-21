# Use Node.js 14 as the base image for building
FROM node:14 as build

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json into the working directory
COPY package*.json ./

# Install dependencies, including the updated Babel version
RUN npm install @babel/core@7.16.0 babel-preset-react-app@10.0.0

# Install the rest of the dependencies
RUN npm install

# Copy the entire application code into the container
COPY . .

# Build the React app
RUN npm run build

# Use a lightweight Node.js image to serve the production build
FROM node:14-alpine

# Install the 'serve' package globally for serving the app
RUN npm install -g serve

# Set the working directory for serving the app
WORKDIR /app

# Copy the build output from the previous stage
COPY --from=build /app/build .

# Expose port 3000 to make the app accessible
EXPOSE 3000

# Define a health check to ensure the app is running
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:3000 || exit 1

# Start the app using 'serve'
CMD ["serve", "-s", ".", "-l", "3000"]
