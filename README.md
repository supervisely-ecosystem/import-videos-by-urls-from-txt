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
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-videos-by-urls-from-txt&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-videos-by-urls-from-txt&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-videos-by-urls-from-txt&counter=runs&label=runs)](https://supervise.ly)

</div>

## Overview

App downloads videos and then uploads them to Supervisely Storage. Video file has to be in Supervisely's internal storage to provide fast processing speed during labeling.

## How To Use

1. Create new team on `source` instance. Copy project to this team. Let's call this project: `project_to_share`.
2. Create and invite user to this team. This new User has access only to projects in special team, all data in other teams is private.
3. Share `id` of `project_to_share` and user's `api_token` with your labeling provider.
4. Labeling provider has to run app and in modal window define `SERVER_ADDRESS`, `id` of project that should be copied and `API_TOKEN`.

<img src="https://i.imgur.com/7hdsoSU.png" width="450px"/>

5. Project (images/annotations/images metadata) is copied to current team/workspace with the same name.  

<img src="https://i.imgur.com/bBqPCZh.png"/>
