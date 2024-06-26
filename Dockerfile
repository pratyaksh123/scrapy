# dependencies
sudo wget https://launchpad.net/~canonical-chromium-builds/+archive/ubuntu/stage/+files/chromium-codecs-ffmpeg_96.0.4664.110-0ubuntu0.18.04.1_arm64.deb
sudo wget https://launchpad.net/~canonical-chromium-builds/+archive/ubuntu/stage/+files/chromium-codecs-ffmpeg-extra_96.0.4664.110-0ubuntu0.18.04.1_arm64.deb

# chromium-browser
sudo wget https://launchpad.net/~canonical-chromium-builds/+archive/ubuntu/stage/+files/chromium-browser_96.0.4664.110-0ubuntu0.18.04.1_arm64.deb

# chromium-chromedriver
sudo wget https://launchpad.net/~canonical-chromium-builds/+archive/ubuntu/stage/+files/chromium-chromedriver_96.0.4664.110-0ubuntu0.18.04.1_arm64.deb

# Install all
sudo apt-get update
sudo apt-get install -y ./chromium-codecs-ffmpeg_96.0.4664.110-0ubuntu0.18.04.1_arm64.deb 
sudo apt-get install -y. /chromium-codecs-ffmpeg-extra_96.0.4664.110-0ubuntu0.18.04.1_arm64.deb 
sudo apt-get install -y ./chromium-browser_96.0.4664.110-0ubuntu0.18.04.1_arm64.deb 
sudo apt-get install -y ./chromium-chromedriver_96.0.4664.110-0ubuntu0.18.04.1_arm64.deb

# Install selenium
pip install -U pip
pip install selenium
