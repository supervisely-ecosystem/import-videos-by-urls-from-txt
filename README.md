<div align="center" markdown>
<img src="https://i.imgur.com/6T1dXGq.png"/>

# Import Videos by URLs from text file

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a>
</p>


[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/import-videos-by-urls-from-txt)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-videos-by-urls-from-txt)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/import-videos-by-urls-from-txt)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/import-videos-by-urls-from-txt)](https://supervise.ly)

</div>

## Overview

App downloads videos and then uploads them to Supervisely Storage. Video file has to be in Supervisely's internal storage to provide fast processing speed during labeling.



## How To Use

**Step 1:** Create text file with URLs to videos - each link on the line. For example `import_01.txt` with the following content: 
```
https://www.google.com/abcd.mp4
https://ia800503.us.archive.org/29/items/meet_john_doe/meet_john_doe_512kb.mp4
https://ia800203.us.archive.org/18/items/house_on_haunted_hill_ipod/house_on_haunted_hill_512kb.mp4
https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4
https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4
```

**Step 2:** Drag and drop this file to Team Files

**Step 3:** Run app from the context menu of file: `context menu` -> `Run App` -> `Import videos by URLs from txt file`

<img src="https://i.imgur.com/GYprBRr.png"/>

**Step 4:** Define the name of destination project and dataset in modal window. If project doesn't exist it will be created. Project will be created in the current workspace. If you would like to change workspace, change active workspace in left sidebar and run the app again.

<img src="https://i.imgur.com/CfpPCWv.png" width="500px"/>

**Step 5:** Monitor progress of task in workspace tasks table. All warning and additional logs can be found in `Task Log`.

<img src="https://i.imgur.com/0TaQRR4.png"/>
