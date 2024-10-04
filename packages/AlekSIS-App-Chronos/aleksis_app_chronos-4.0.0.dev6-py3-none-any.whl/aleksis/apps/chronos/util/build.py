from collections import OrderedDict
from datetime import date, datetime, time
from typing import Union

from django.apps import apps

from calendarweek import CalendarWeek

from aleksis.apps.chronos.managers import TimetableType
from aleksis.apps.chronos.models import SupervisionEvent
from aleksis.core.models import Group, Person, Room

LessonPeriod = apps.get_model("chronos", "LessonPeriod")
LessonEvent = apps.get_model("chronos", "LessonEvent")
TimePeriod = apps.get_model("chronos", "TimePeriod")
Break = apps.get_model("chronos", "Break")
Supervision = apps.get_model("chronos", "Supervision")
LessonSubstitution = apps.get_model("chronos", "LessonSubstitution")
SupervisionSubstitution = apps.get_model("chronos", "SupervisionSubstitution")
Event = apps.get_model("chronos", "Event")
Holiday = apps.get_model("chronos", "Holiday")
ExtraLesson = apps.get_model("chronos", "ExtraLesson")


def build_timetable(
    type_: Union[TimetableType, str],
    obj: Union[Group, Room, Person],
    date_ref: Union[CalendarWeek, date],
    with_holidays: bool = True,
):
    needed_breaks = []

    is_person = False
    if type_ == "person":
        is_person = True
        type_ = obj.timetable_type

    is_week = False
    if isinstance(date_ref, CalendarWeek):
        is_week = True

    if type_ is None:
        return None

    # Get matching holidays
    if is_week:
        holidays_per_weekday = Holiday.in_week(date_ref) if with_holidays else {}
    else:
        holiday = Holiday.on_day(date_ref) if with_holidays else None

    # Get matching lesson periods
    lesson_periods = LessonPeriod.objects
    lesson_periods = (
        lesson_periods.select_related(None)
        .select_related("lesson", "lesson__subject", "period", "room")
        .only(
            "lesson",
            "period",
            "room",
            "lesson__subject",
            "period__weekday",
            "period__period",
            "lesson__subject__short_name",
            "lesson__subject__name",
            "lesson__subject__colour_fg",
            "lesson__subject__colour_bg",
            "room__short_name",
            "room__name",
        )
    )

    if is_week:
        lesson_periods = lesson_periods.in_week(date_ref)
    else:
        lesson_periods = lesson_periods.on_day(date_ref)

    if is_person:
        lesson_periods = lesson_periods.filter_from_person(obj)
    else:
        lesson_periods = lesson_periods.filter_from_type(type_, obj, is_smart=with_holidays)

    # Sort lesson periods in a dict
    lesson_periods_per_period = lesson_periods.group_by_periods(is_week=is_week)

    # Get events
    extra_lessons = ExtraLesson.objects
    if is_week:
        extra_lessons = extra_lessons.filter(week=date_ref.week, year=date_ref.year)
    else:
        extra_lessons = extra_lessons.on_day(date_ref)
    if is_person:
        extra_lessons = extra_lessons.filter_from_person(obj)
    else:
        extra_lessons = extra_lessons.filter_from_type(type_, obj)

    extra_lessons = extra_lessons.only(
        "week",
        "year",
        "period",
        "subject",
        "room",
        "comment",
        "period__weekday",
        "period__period",
        "subject__short_name",
        "subject__name",
        "subject__colour_fg",
        "subject__colour_bg",
        "room__short_name",
        "room__name",
    )

    # Sort lesson periods in a dict
    extra_lessons_per_period = extra_lessons.group_by_periods(is_week=is_week)

    # Get events
    events = Event.objects
    events = events.in_week(date_ref) if is_week else events.on_day(date_ref)

    events = events.only(
        "id",
        "title",
        "date_start",
        "date_end",
        "period_from",
        "period_to",
        "period_from__weekday",
        "period_from__period",
        "period_to__weekday",
        "period_to__period",
    )

    if is_person:
        events_to_display = events.filter_from_person(obj)
    else:
        events_to_display = events.filter_from_type(type_, obj)

    # Sort events in a dict
    events_per_period = {}
    events_for_replacement_per_period = {}
    for event in events:
        if is_week and event.date_start < date_ref[TimePeriod.weekday_min]:
            # If start date not in current week, set weekday and period to min
            weekday_from = TimePeriod.weekday_min
            period_from_first_weekday = TimePeriod.period_min
        else:
            weekday_from = event.date_start.weekday()
            period_from_first_weekday = event.period_from.period

        if is_week and event.date_end > date_ref[TimePeriod.weekday_max]:
            # If end date not in current week, set weekday and period to max
            weekday_to = TimePeriod.weekday_max
            period_to_last_weekday = TimePeriod.period_max
        else:
            weekday_to = event.date_end.weekday()
            period_to_last_weekday = event.period_to.period

        for weekday in range(weekday_from, weekday_to + 1):
            if not is_week and weekday != date_ref.weekday():
                # If daily timetable for person, skip other weekdays
                continue

            # If start day, use start period else use min period
            period_from = (
                period_from_first_weekday if weekday == weekday_from else TimePeriod.period_min
            )

            # If end day, use end period else use max period
            period_to = period_to_last_weekday if weekday == weekday_to else TimePeriod.periox_max

            for period in range(period_from, period_to + 1):
                # The following events are possibly replacing some lesson periods
                if period not in events_for_replacement_per_period:
                    events_for_replacement_per_period[period] = {} if is_week else []

                if is_week and weekday not in events_for_replacement_per_period[period]:
                    events_for_replacement_per_period[period][weekday] = []

                if not is_week:
                    events_for_replacement_per_period[period].append(event)
                else:
                    events_for_replacement_per_period[period][weekday].append(event)

                # and the following will be displayed in the timetable
                if event in events_to_display:
                    if period not in events_per_period:
                        events_per_period[period] = {} if is_week else []

                    if is_week and weekday not in events_per_period[period]:
                        events_per_period[period][weekday] = []

                    if not is_week:
                        events_per_period[period].append(event)
                    else:
                        events_per_period[period][weekday].append(event)

    if type_ == TimetableType.TEACHER:
        # Get matching supervisions
        week = CalendarWeek.from_date(date_ref) if not is_week else date_ref
        supervisions = (
            Supervision.objects.in_week(week)
            .all()
            .annotate_week(week)
            .filter_by_teacher(obj)
            .only(
                "area",
                "break_item",
                "teacher",
                "area",
                "area__short_name",
                "area__name",
                "area__colour_fg",
                "area__colour_bg",
                "break_item__short_name",
                "break_item__name",
                "break_item__after_period__period",
                "break_item__after_period__weekday",
                "break_item__before_period__period",
                "break_item__before_period__weekday",
                "teacher__short_name",
                "teacher__first_name",
                "teacher__last_name",
            )
        )

        if not is_week:
            supervisions = supervisions.filter_by_weekday(date_ref.weekday())

        supervisions_per_period_after = {}
        for supervision in supervisions:
            weekday = supervision.break_item.weekday
            period_after_break = supervision.break_item.before_period_number

            if period_after_break not in needed_breaks:
                needed_breaks.append(period_after_break)

            if is_week and period_after_break not in supervisions_per_period_after:
                supervisions_per_period_after[period_after_break] = {}

            if not is_week:
                supervisions_per_period_after[period_after_break] = supervision
            else:
                supervisions_per_period_after[period_after_break][weekday] = supervision

    # Get ordered breaks
    breaks = OrderedDict(sorted(Break.get_breaks_dict().items()))

    rows = []
    for period, break_ in breaks.items():  # period is period after break
        # Break
        if type_ == TimetableType.TEACHER and period in needed_breaks:
            row = {
                "type": "break",
                "after_period": break_.after_period_number,
                "before_period": break_.before_period_number,
                "time_start": break_.time_start,
                "time_end": break_.time_end,
            }

            if is_week:
                cols = []

                for weekday in range(TimePeriod.weekday_min, TimePeriod.weekday_max + 1):
                    col = None
                    if (
                        period in supervisions_per_period_after
                        and weekday not in holidays_per_weekday
                    ) and weekday in supervisions_per_period_after[period]:
                        col = supervisions_per_period_after[period][weekday]
                    cols.append(col)

                row["cols"] = cols
            else:
                col = None
                if period in supervisions_per_period_after and not holiday:
                    col = supervisions_per_period_after[period]
                row["col"] = col
            rows.append(row)

        # Period
        if period <= TimePeriod.period_max:
            row = {
                "type": "period",
                "period": period,
                "time_start": break_.before_period.time_start,
                "time_end": break_.before_period.time_end,
            }

            if is_week:
                cols = []
                for weekday in range(TimePeriod.weekday_min, TimePeriod.weekday_max + 1):
                    # Skip this period if there are holidays
                    if weekday in holidays_per_weekday:
                        cols.append([])
                        continue

                    col = []

                    events_for_this_period = (
                        events_per_period[period].get(weekday, [])
                        if period in events_per_period
                        else []
                    )
                    events_for_replacement_for_this_period = (
                        events_for_replacement_per_period[period].get(weekday, [])
                        if period in events_for_replacement_per_period
                        else []
                    )
                    lesson_periods_for_this_period = (
                        lesson_periods_per_period[period].get(weekday, [])
                        if period in lesson_periods_per_period
                        else []
                    )

                    # Add lesson periods
                    if lesson_periods_for_this_period:
                        if events_for_replacement_for_this_period:
                            # If there is a event in this period,
                            # we have to check whether the actual lesson is taking place.

                            for lesson_period in lesson_periods_for_this_period:
                                replaced_by_event = lesson_period.is_replaced_by_event(
                                    events_for_replacement_for_this_period,
                                    [obj] if type_ == TimetableType.GROUP else None,
                                )
                                lesson_period.replaced_by_event = replaced_by_event
                                if not replaced_by_event or (
                                    replaced_by_event and type_ != TimetableType.GROUP
                                ):
                                    col.append(lesson_period)

                        else:
                            col += lesson_periods_for_this_period

                    # Add extra lessons
                    if period in extra_lessons_per_period:
                        col += extra_lessons_per_period[period].get(weekday, [])

                    # Add events
                    col += events_for_this_period

                    cols.append(col)

                row["cols"] = cols
            else:
                col = []

                # Skip this period if there are holidays
                if holiday:
                    continue

                events_for_this_period = events_per_period.get(period, [])
                events_for_replacement_for_this_period = events_for_replacement_per_period.get(
                    period, []
                )
                lesson_periods_for_this_period = lesson_periods_per_period.get(period, [])

                # Add lesson periods
                if lesson_periods_for_this_period:
                    if events_for_replacement_for_this_period:
                        # If there is a event in this period,
                        # we have to check whether the actual lesson is taking place.

                        lesson_periods_to_keep = []
                        for lesson_period in lesson_periods_for_this_period:
                            if not lesson_period.is_replaced_by_event(
                                events_for_replacement_for_this_period
                            ):
                                lesson_periods_to_keep.append(lesson_period)
                        col += lesson_periods_to_keep
                    else:
                        col += lesson_periods_for_this_period

                # Add events and extra lessons
                col += extra_lessons_per_period.get(period, [])
                col += events_for_this_period

                row["col"] = col

            rows.append(row)

    return rows


def build_substitutions_list(wanted_day: date) -> tuple[list[dict], set[Person], set[Group]]:
    rows = []
    affected_teachers = set()
    affected_groups = set()

    lesson_events = LessonEvent.get_single_events(
        datetime.combine(wanted_day, time.min),
        datetime.combine(wanted_day, time.max),
        params={"amending": True},
        with_reference_object=True,
    )

    for lesson_event in lesson_events:
        affected_teachers.update(lesson_event["REFERENCE_OBJECT"].teachers.all())
        affected_teachers.update(lesson_event["REFERENCE_OBJECT"].amends.teachers.all())
        affected_groups.update(lesson_event["REFERENCE_OBJECT"].groups.all())
        affected_groups.update(lesson_event["REFERENCE_OBJECT"].amends.groups.all())

        row = {
            "type": "substitution",
            "sort_a": lesson_event["REFERENCE_OBJECT"].group_names,
            "sort_b": str(lesson_event["DTSTART"]),
            "el": lesson_event,
        }

        rows.append(row)

    supervision_events = SupervisionEvent.get_single_events(
        datetime.combine(wanted_day, time.min),
        datetime.combine(wanted_day, time.max),
        params={"amending": True},
        with_reference_object=True,
    )
    print(supervision_events)

    for supervision_event in supervision_events:
        affected_teachers.update(supervision_event["REFERENCE_OBJECT"].teachers.all())
        affected_teachers.update(supervision_event["REFERENCE_OBJECT"].amends.teachers.all())

        row = {
            "type": "supervision_substitution",
            "sort_a": "Z",
            "sort_b": str(supervision_event["DTSTART"]),
            "el": supervision_event,
        }

        rows.append(row)

    rows.sort(key=lambda row: row["sort_a"] + row["sort_b"])

    return rows, affected_teachers, affected_groups


def build_weekdays(
    base: list[tuple[int, str]], wanted_week: CalendarWeek, with_holidays: bool = True
) -> list[dict]:
    if with_holidays:
        holidays_per_weekday = Holiday.in_week(wanted_week)

    weekdays = []
    for key, name in base[TimePeriod.weekday_min : TimePeriod.weekday_max + 1]:
        weekday = {
            "key": key,
            "name": name,
            "date": wanted_week[key],
        }
        if with_holidays:
            weekday["holiday"] = holidays_per_weekday[key] if key in holidays_per_weekday else None
        weekdays.append(weekday)

    return weekdays
