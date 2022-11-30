# Open Conference URL

*Copyright 2020-2022 Caleb Evans*  
*Released under the MIT license*

[![tests](https://github.com/caleb531/open-conference-url/actions/workflows/tests.yml/badge.svg)](https://github.com/caleb531/open-conference-url/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/caleb531/open-conference-url/badge.svg?branch=main)](https://coveralls.io/r/caleb531/open-conference-url?branch=main)

Open Conference URL is an [Alfred][alfred] workflow which enables you to quickly
open links for Zoom and other conferencing services, based on your upcoming
calendar events.

[alfred]: https://www.alfredapp.com/

![Screenshot](screenshot.png)

## Installation

To download the workflow, simply click the download link below.

[Download Open Conference URL (Alfred 5)][workflow-download-alfred5]

[workflow-download-alfred5]: https://github.com/caleb531/open-conference-url/raw/main/Open%20Conference%20URL%20(Alfred%205).alfredworkflow

[Download Open Conference URL (Alfred 4)][workflow-download-alfred4]

[workflow-download-alfred4]: https://github.com/caleb531/open-conference-url/raw/main/Open%20Conference%20URL%20(Alfred%204).alfredworkflow

## Usage

To use, simply type the `conf` command into Alfred, and you will see a list of
upcoming calendar events. It does this by including all events within +/- 20
minutes of your system's current time, so even if you're running late to a
meeting, the logical event will show.

The workflow also accounts for timezones and Daylight Saving Time (DST). All
times are displayed in your system's local timezone.

## Configuration

This workflow contains configuration for various aspects of the workflow's
behavior. In Alfred 5, you can adjust these configuration options by navigating
to the workflow in Alfred Preferences and clicking the "Configure Workflow..."
button near the top of the window.

### conference_domains

The `conference_domains` option is a comma-separated list of domain names
representing which URLs to check within each calendar event. This domains list
determines which links are considered "conference" URLs.

The domains are listed in order of precedence, so if `zoom.us` precedes
`google.com` in the list, then the workflow will prefer Zoom links over Google
Meet links if both are present in a calendar event.

If you wish to match a subdomain, you must specify it explicitly (e.g.
`teams.microsoft.com`). However, you can also match all subdomains via the
asterisk character (`*`) as a wildcard (e.g. `*.zoom.us`).

### calendar_names

The `calendar_names` option is a comma-separated list of calendar names on your
local system for which to fetch events. If you leave this field blank, then the
workflow will implicitly fetch check all calendars for event data.

### event_time_threshold_mins

The `event_time_threshold_mins` is an integer representing the number of
minutes before/after a meeting. If an event is within this duration of time
(relative to the system's current time), it will be displayed in Alfred's
results.

For example, a value of `30` will mean the workflow will only show
events whose start time was within the last 30 minutes *or* whose start time is
within the next 20 minutes.

### use_direct_zoom

The `use_direct_zoom` option opens Zoom links directly in the Zoom application,
bypassing the browser entirely.

### use_direct_msteams

The `use_direct_msteams` option opens Microsoft Teams links directly in the
Microsoft Teams application, bypassing the browser entirely.

## Credits

Kudos to [@jacksonrayhamilton][jrh] for his architecture ideas and feedback on
this project.

[jrh]: https://github.com/jacksonrayhamilton
