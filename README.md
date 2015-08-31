# vk_last_fm
Download tracks loved in last.fm via VK API.

## This application does 2 major things:
####  - last_fm.py
  - gets list of friends 
  - gets list of loved trackd for each of them
  - checks which artists have low play-count (no reason to download songs of artists you alreasy listen to)
  - accumulate list for download
  
####    - vk.py
  - gets tracks from lists
