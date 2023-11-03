# Use the specified Python base image
FROM python:3.11

# Explicitly copy autorun.sh and then the rest of the files
COPY . .

# Update pip and install required Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Ensure that autorun.sh is executable
RUN chmod +x ./autorun.sh

# Expose the specified port
EXPOSE 6789

# Set the entrypoint to the script
ENTRYPOINT ["bash","./autorun.sh"]
