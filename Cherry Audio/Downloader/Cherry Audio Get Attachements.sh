#!/bin/bash 

urlArray=(
"https://store.cherryaudio.com/downloads/ca2600-macos-installer"
"https://store.cherryaudio.com/downloads/chroma-macos-installer"
"https://store.cherryaudio.com/downloads/cr-78-macos-installer"
"https://store.cherryaudio.com/downloads/dco-106-macos-installer"
"https://store.cherryaudio.com/downloads/dreamsynth-macos-installer"
"https://store.cherryaudio.com/downloads/eight-voice-macos-installer"
"https://store.cherryaudio.com/downloads/elka-x-macos-installer"
"https://store.cherryaudio.com/downloads/galactic-reverb-macos-installer"
"https://store.cherryaudio.com/downloads/gx-80-macos-installer"
"https://store.cherryaudio.com/downloads/harmonia-macos-installer"
"https://store.cherryaudio.com/downloads/lowdown-macos-installer"
"https://store.cherryaudio.com/downloads/memorymode-macos-installer"
"https://store.cherryaudio.com/downloads/mercury-4-macos-installer"
"https://store.cherryaudio.com/downloads/mercury-6-macos-installer"
"https://store.cherryaudio.com/downloads/miniverse-macos-installer"
"https://store.cherryaudio.com/downloads/novachord-macos-installer"
"https://store.cherryaudio.com/downloads/octave-cat-macos-installer"
"https://store.cherryaudio.com/downloads/polymode-synthesizer-macos-installer"
"https://store.cherryaudio.com/downloads/pro-soloist-macos-installer"
"https://store.cherryaudio.com/downloads/ps-20-macos-installer"
"https://store.cherryaudio.com/downloads/ps-3300-macos-installer"
"https://store.cherryaudio.com/downloads/quadra-macos-installer"
"https://store.cherryaudio.com/downloads/rackmode-macos-installer"
"https://store.cherryaudio.com/downloads/sines-macos-installer"
"https://store.cherryaudio.com/downloads/solovox-macos-installer"
"https://store.cherryaudio.com/downloads/stardust-201-macos-installer"
"https://store.cherryaudio.com/downloads/surrealistic-mg-1-plus-macos-installer"
"https://store.cherryaudio.com/downloads/sync-macos-installer"
"https://store.cherryaudio.com/downloads/synthesizer-expander-module-macos-installer"
"https://store.cherryaudio.com/downloads/wurlybird140b-macos-installer"
"https://store.cherryaudio.com/voltage-mac/download"
"https://store.cherryaudio.com/module-designer-mac/download"
)


for url in ${urlArray[@]}; do
  echo "$url"
  echo "$url" | cut -d/ -f5 | cut -d- -f1-3
  echo "$url" | cut -d/ -f4-5
  attachementName=$(curl -I -s "$url" | grep attachment | sed -r 's/.*"(.*)".*/\1/')
  echo "$attachementName"
  echo "$url?file=$attachementName"
  echo
done
