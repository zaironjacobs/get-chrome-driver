FROM python:3.11

# Set workdir
WORKDIR /app

# Install Chrome dependencies
RUN apt update && apt install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1

# Download Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install Chrome
RUN apt install -y ./google-chrome-stable_current_amd64.deb

# Copy test requirements
COPY requirements-test.txt .

# Install test requirements
RUN pip install --no-cache-dir --upgrade -r requirements-test.txt

# Copy app
COPY . .

# Install app
RUN pip install --no-cache-dir --upgrade .
