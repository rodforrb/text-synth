#!/bin/sh
if [ ! -d "model-fa" ]; then
  echo "Downloading Farsi Model"
  wget https://alphacephei.com/vosk/models/vosk-model-small-fa-0.5.zip -O model-fa.zip
  unzip model-fa.zip -d model-fa-temp
  mv model-fa-temp/vosk-model-small-fa-0.5 model-fa
  rm -r model-fa-temp
  rm model-fa.zip
else
  echo "Farsi Model already present."
fi

# if [ ! -d "model-en" ]; then
#   echo "Downloading English Model"
#   wget https://alphacephei.com/vosk/models/vosk-model-en-us-aspire-0.2.zip -O model-en.zip
#   unzip model-en.zip -d model-en-temp
#   mv model-en-temp/vosk-model-en-us-aspire-0.2 model-en
#   rm -r model-en-temp
#   rm model-en.zip
# else
#   echo "English Model already present."
# fi
