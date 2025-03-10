#!/usr/bin/env python3

import json
import unittest

from freezegun import freeze_time

from ocu import list_events
from tests.decorators import redirect_stdout, use_env, use_event_dicts

case = unittest.TestCase()


@use_event_dicts([{
    'title': 'My Meeting',
    'startDate': '2022-10-16T08:00',
    'endDate': '2022-10-16T09:00',
    'location': 'https://zoom.us/j/123456'
}])
@freeze_time('2022-10-16 07:55:00')
@redirect_stdout
def test_5mins_before(out, event_dicts):
    """Should list meeting starting in 5 minutes"""
    list_events.main()
    feedback = json.loads(out.getvalue())
    case.assertEqual(feedback['items'][0]['title'], 'My Meeting')
    case.assertEqual(feedback['items'][0]['subtitle'], '8:00am')
    case.assertEqual(
        feedback['items'][0]['text']['copy'],
        event_dicts[0]['location'])
    case.assertEqual(
        feedback['items'][0]['text']['largetype'],
        event_dicts[0]['location'])
    case.assertEqual(len(feedback['items']), 1)


@use_event_dicts([{
    'title': 'My Meeting',
    'startDate': '2022-10-16T08:00',
    'endDate': '2022-10-16T09:00',
    'location': 'https://zoom.us/j/123456'
}])
@freeze_time('2022-10-16 8:05:00')
@redirect_stdout
def test_5mins_after(out, event_dicts):
    """Should list meeting that started 5 minutes ago"""
    list_events.main()
    feedback = json.loads(out.getvalue())
    case.assertEqual(feedback['items'][0]['title'], 'My Meeting')
    case.assertEqual(feedback['items'][0]['subtitle'], '8:00am')
    case.assertEqual(
        feedback['items'][0]['text']['copy'],
        event_dicts[0]['location'])
    case.assertEqual(
        feedback['items'][0]['text']['largetype'],
        event_dicts[0]['location'])
    case.assertEqual(len(feedback['items']), 1)


@use_event_dicts([{
    'title': 'My Meeting',
    'startDate': '2022-10-16T08:00',
    'endDate': '2022-10-16T09:00',
    'location': 'https://zoom.us/j/123456'
}])
@freeze_time('2022-10-16 7:30:00')
@redirect_stdout
def test_before_window(out, event_dicts):
    """Should list all meetings if before next meeting's window"""
    list_events.main()
    feedback = json.loads(out.getvalue())
    case.assertEqual(feedback['items'][0]['title'], 'No Upcoming Meetings')
    case.assertEqual(feedback['items'][1]['title'], 'My Meeting')
    case.assertEqual(
        feedback['items'][1]['text']['copy'],
        event_dicts[0]['location'])
    case.assertEqual(
        feedback['items'][1]['text']['largetype'],
        event_dicts[0]['location'])
    case.assertEqual(len(feedback['items']), 2)


@use_event_dicts([{
    'title': 'My Meeting',
    'startDate': '2022-10-16T08:00',
    'endDate': '2022-10-16T09:00',
    'location': 'https://zoom.us/j/123456'
}])
@freeze_time('2022-10-16 9:30:00')
@redirect_stdout
def test_after_window(out, event_dicts):
    """Should list all meetings if after next meeting's window"""
    list_events.main()
    feedback = json.loads(out.getvalue())
    case.assertEqual(feedback['items'][0]['title'], 'No Upcoming Meetings')
    case.assertEqual(feedback['items'][1]['title'], 'My Meeting')
    case.assertEqual(
        feedback['items'][1]['text']['copy'],
        event_dicts[0]['location'])
    case.assertEqual(
        feedback['items'][1]['text']['largetype'],
        event_dicts[0]['location'])
    case.assertEqual(len(feedback['items']), 2)


@use_event_dicts([{
    'title': 'All-Day Conference',
    'startDate': '2022-10-16T00:00',
    'isAllDay': 'true',
    'location': 'https://zoom.us/j/123456'
}])
@freeze_time('2022-10-16 8:00:00')
@redirect_stdout
def test_all_day_standalone(out, event_dicts):
    """Should list all-day meetings by themselves"""
    list_events.main()
    feedback = json.loads(out.getvalue())
    case.assertEqual(feedback['items'][0]['title'], 'All-Day Conference')
    case.assertEqual(feedback['items'][0]['subtitle'], 'All-Day')
    case.assertEqual(
        feedback['items'][0]['text']['copy'],
        event_dicts[0]['location'])
    case.assertEqual(
        feedback['items'][0]['text']['largetype'],
        event_dicts[0]['location'])
    case.assertEqual(len(feedback['items']), 1)


@use_event_dicts([
    {
        'title': 'All-Day Conference',
        'startDate': '2022-10-16T00:00',
        'isAllDay': 'true',
        'location': 'https://zoom.us/j/123456'
    },
    {
        'title': 'Morning Scrum',
        'startDate': '2022-10-16T08:00',
        'endDate': '2022-10-16T09:00',
        'location': 'https://zoom.us/j/789012'
    }
])
@freeze_time('2022-10-16 7:58:00')
@redirect_stdout
def test_all_day_mixed(out, event_dicts):
    """Should list all-day meetings alongside upcoming meetings"""
    list_events.main()
    feedback = json.loads(out.getvalue())
    case.assertEqual(feedback['items'][0]['title'], 'All-Day Conference')
    case.assertEqual(feedback['items'][0]['subtitle'], 'All-Day')
    case.assertEqual(
        feedback['items'][0]['text']['copy'],
        event_dicts[0]['location'])
    case.assertEqual(
        feedback['items'][0]['text']['largetype'],
        event_dicts[0]['location'])
    case.assertEqual(feedback['items'][1]['title'], 'Morning Scrum')
    case.assertEqual(feedback['items'][1]['subtitle'], '8:00am')
    case.assertEqual(
        feedback['items'][1]['text']['copy'],
        event_dicts[1]['location'])
    case.assertEqual(
        feedback['items'][1]['text']['largetype'],
        event_dicts[1]['location'])
    case.assertEqual(len(feedback['items']), 2)


@use_event_dicts([
    {
        'title': 'My Meeting 1',
        'startDate': '2022-10-16T08:00',
        'endDate': '2022-10-16T09:00',
        'location': 'https://zoom.us/j/123456'
    },
    {
        'title': 'My Meeting 2',
        'startDate': '2022-10-16T08:00',
        'endDate': '2022-10-16T09:00',
        'location': 'https://zoom.us/j/789012'
    }
])
@freeze_time('2022-10-16 07:55:00')
@redirect_stdout
def test_multiple_meetings_at_once(out, event_dicts):
    """Should list multiple upcoming meetings at once"""
    list_events.main()
    feedback = json.loads(out.getvalue())
    case.assertEqual(feedback['items'][0]['title'], 'My Meeting 1')
    case.assertEqual(feedback['items'][0]['subtitle'], '8:00am')
    case.assertEqual(
        feedback['items'][0]['text']['copy'],
        event_dicts[0]['location'])
    case.assertEqual(
        feedback['items'][0]['text']['largetype'],
        event_dicts[0]['location'])
    case.assertEqual(feedback['items'][1]['title'], 'My Meeting 2')
    case.assertEqual(feedback['items'][1]['subtitle'], '8:00am')
    case.assertEqual(
        feedback['items'][1]['text']['copy'],
        event_dicts[1]['location'])
    case.assertEqual(
        feedback['items'][1]['text']['largetype'],
        event_dicts[1]['location'])
    case.assertEqual(len(feedback['items']), 2)


@use_event_dicts([
    {
        'title': 'My Meeting',
        'startDate': '2022-10-16T08:00',
        'endDate': '2022-10-16T09:00',
        'location': 'https://zoom.us/j/123456'
    },
    {
        'title': 'My Non-Meeting',
        'startDate': '2022-10-16T08:00',
        'endDate': '2022-10-16T09:00',
        'location': 'https://github.com'
    }
])
@freeze_time('2022-10-16 07:55:00')
@redirect_stdout
def test_excluding_non_conference_urls(out, event_dicts):
    """Should exclude non-conference URLs from 'upcoming' results"""
    list_events.main()
    feedback = json.loads(out.getvalue())
    case.assertEqual(feedback['items'][0]['title'], 'My Meeting')
    case.assertEqual(feedback['items'][0]['subtitle'], '8:00am')
    case.assertEqual(
        feedback['items'][0]['text']['copy'],
        event_dicts[0]['location'])
    case.assertEqual(
        feedback['items'][0]['text']['largetype'],
        event_dicts[0]['location'])
    case.assertEqual(len(feedback['items']), 1)


@use_event_dicts([])
@freeze_time('2022-10-16 9:30:00')
@redirect_stdout
def test_no_events_for_today(out, event_dicts):
    """Should display no meetings if there are no events for today"""
    list_events.main()
    feedback = json.loads(out.getvalue())
    case.assertEqual(feedback['items'][0]['title'], 'No Results')
    case.assertEqual(len(feedback['items']), 1)


@use_env('time_system', '24-hour')
@use_event_dicts([{
    'title': 'My Meeting',
    'startDate': '2022-10-16T13:00',
    'endDate': '2022-10-16T14:00',
    'location': 'https://zoom.us/j/123456'
}])
@freeze_time('2022-10-16 12:55:00')
@redirect_stdout
def test_24_hour(out, event_dicts):
    """Should list meeting starting in 5 minutes"""
    list_events.main()
    feedback = json.loads(out.getvalue())
    case.assertEqual(feedback['items'][0]['title'], 'My Meeting')
    case.assertEqual(feedback['items'][0]['subtitle'], '13:00')
    case.assertEqual(
        feedback['items'][0]['text']['copy'],
        event_dicts[0]['location'])
    case.assertEqual(
        feedback['items'][0]['text']['largetype'],
        event_dicts[0]['location'])
    case.assertEqual(len(feedback['items']), 1)
