# Use the official Nginx image
FROM nginx:latest

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy your Nginx configuration
COPY nginx/nginx.conf /etc/nginx/conf.d

# Copy the built React app (static files)
COPY build/ /usr/share/nginx/html/

# Copy the image directory (if needed)
COPY images/ /usr/share/nginx/html/images/

# Expose port 80 for the web
EXPOSE 8080