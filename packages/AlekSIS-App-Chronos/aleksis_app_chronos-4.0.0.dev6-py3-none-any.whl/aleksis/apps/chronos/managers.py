from collections.abc import Iterable
from datetime import date, datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING, Optional, Union

from django.db import models
from django.db.models import ExpressionWrapper, F, Func, Q, QuerySet, Value
from django.db.models.fields import DateField
from django.db.models.functions import Concat

from calendarweek import CalendarWeek

from aleksis.apps.chronos.util.date import week_weekday_from_date, week_weekday_to_date
from aleksis.apps.cursus.models import Course
from aleksis.core.managers import (
    AlekSISBaseManagerWithoutMigrations,
    DateRangeQuerySetMixin,
    RecurrencePolymorphicQuerySet,
    SchoolTermRelatedQuerySet,
)
from aleksis.core.models import Group, Person, Room
from aleksis.core.util.core_helpers import get_site_preferences

if TYPE_CHECKING:
    from .models import Holiday, LessonPeriod, ValidityRange


class ValidityRangeQuerySet(QuerySet, DateRangeQuerySetMixin):
    """Custom query set for validity ranges."""


class ValidityRangeRelatedQuerySet(QuerySet):
    """Custom query set for all models related to validity ranges."""

    def within_dates(self, start: date, end: date) -> "ValidityRangeRelatedQuerySet":
        """Filter for all objects within a date range."""
        return self.filter(validity__date_start__lte=end, validity__date_end__gte=start)

    def in_week(self, wanted_week: CalendarWeek) -> "ValidityRangeRelatedQuerySet":
        """Filter for all objects within a calendar week."""
        return self.within_dates(wanted_week[0], wanted_week[6])

    def on_day(self, day: date) -> "ValidityRangeRelatedQuerySet":
        """Filter for all objects on a certain day."""
        return self.within_dates(day, day)

    def for_validity_range(self, validity_range: "ValidityRange") -> "ValidityRangeRelatedQuerySet":
        return self.filter(validity=validity_range)

    def for_current_or_all(self) -> "ValidityRangeRelatedQuerySet":
        """Get all objects related to current validity range.

        If there is no current validity range, it will return all objects.
        """
        from aleksis.apps.chronos.models import ValidityRange

        current_validity_range = ValidityRange.current
        if current_validity_range:
            return self.for_validity_range(current_validity_range)
        else:
            return self

    def for_current_or_none(self) -> Union["ValidityRangeRelatedQuerySet", None]:
        """Get all objects related to current validity range.

        If there is no current validity range, it will return `None`.
        """
        from aleksis.apps.chronos.models import ValidityRange

        current_validity_range = ValidityRange.current
        if current_validity_range:
            return self.for_validity_range(current_validity_range)
        else:
            return None


class TimetableType(Enum):
    """Enum for different types of timetables."""

    GROUP = "group"
    TEACHER = "teacher"
    ROOM = "room"

    @classmethod
    def from_string(cls, s: Optional[str]):
        return cls.__members__.get(s.upper())


class LessonPeriodManager(AlekSISBaseManagerWithoutMigrations):
    """Manager adding specific methods to lesson periods."""

    def get_queryset(self):
        """Ensure all related lesson data is loaded as well."""
        return (
            super()
            .get_queryset()
            .select_related(
                "lesson",
                "lesson__subject",
                "period",
                "room",
                "lesson__validity",
                "lesson__validity__school_term",
            )
            .prefetch_related(
                "lesson__groups",
                "lesson__groups__parent_groups",
                "lesson__teachers",
                "substitutions",
            )
        )


class LessonSubstitutionManager(AlekSISBaseManagerWithoutMigrations):
    """Manager adding specific methods to lesson substitutions."""

    def get_queryset(self):
        """Ensure all related lesson data is loaded as well."""
        return (
            super()
            .get_queryset()
            .select_related(
                "lesson_period",
                "lesson_period__lesson",
                "lesson_period__lesson__subject",
                "subject",
                "lesson_period__period",
                "room",
                "lesson_period__room",
            )
            .prefetch_related(
                "lesson_period__lesson__groups",
                "lesson_period__lesson__groups__parent_groups",
                "teachers",
                "lesson_period__lesson__teachers",
            )
        )


class SupervisionManager(AlekSISBaseManagerWithoutMigrations):
    """Manager adding specific methods to supervisions."""

    def get_queryset(self):
        """Ensure all related data is loaded as well."""
        return (
            super()
            .get_queryset()
            .select_related(
                "teacher",
                "area",
                "break_item",
                "break_item__after_period",
                "break_item__before_period",
            )
        )


class SupervisionSubstitutionManager(AlekSISBaseManagerWithoutMigrations):
    """Manager adding specific methods to supervision substitutions."""

    def get_queryset(self):
        """Ensure all related data is loaded as well."""
        return (
            super()
            .get_queryset()
            .select_related(
                "teacher",
                "supervision",
                "supervision__teacher",
                "supervision__area",
                "supervision__break_item",
                "supervision__break_item__after_period",
                "supervision__break_item__before_period",
            )
        )


class EventManager(AlekSISBaseManagerWithoutMigrations):
    """Manager adding specific methods to events."""

    def get_queryset(self):
        """Ensure all related data is loaded as well."""
        return (
            super()
            .get_queryset()
            .select_related("period_from", "period_to")
            .prefetch_related(
                "groups",
                "groups__school_term",
                "groups__parent_groups",
                "teachers",
                "rooms",
            )
        )


class ExtraLessonManager(AlekSISBaseManagerWithoutMigrations):
    """Manager adding specific methods to extra lessons."""

    def get_queryset(self):
        """Ensure all related data is loaded as well."""
        return (
            super()
            .get_queryset()
            .select_related("room", "period", "subject")
            .prefetch_related(
                "groups",
                "groups__school_term",
                "groups__parent_groups",
                "teachers",
            )
        )


class BreakManager(AlekSISBaseManagerWithoutMigrations):
    """Manager adding specific methods to breaks."""

    def get_queryset(self):
        """Ensure all related data is loaded as well."""
        return super().get_queryset().select_related("before_period", "after_period")


class WeekQuerySetMixin:
    def annotate_week(self, week: Union[CalendarWeek]):
        """Annotate all lessons in the QuerySet with the number of the provided calendar week."""
        return self.annotate(
            _week=models.Value(week.week, models.IntegerField()),
            _year=models.Value(week.year, models.IntegerField()),
        )

    def alias_week(self, week: Union[CalendarWeek]):
        """Add an alias to all lessons in the QuerySet with the number of the calendar week."""
        return self.alias(
            _week=models.Value(week.week, models.IntegerField()),
            _year=models.Value(week.year, models.IntegerField()),
        )


class GroupByPeriodsMixin:
    def group_by_periods(self, is_week: bool = False) -> dict:
        """Group a QuerySet of objects with attribute period by period numbers and weekdays."""
        per_period = {}
        for obj in self:
            period = obj.period.period
            weekday = obj.period.weekday

            if period not in per_period:
                per_period[period] = [] if not is_week else {}

            if is_week and weekday not in per_period[period]:
                per_period[period][weekday] = []

            if not is_week:
                per_period[period].append(obj)
            else:
                per_period[period][weekday].append(obj)

        return per_period


class LessonDataQuerySet(models.QuerySet, WeekQuerySetMixin):
    """Overrides default QuerySet to add specific methods for lesson data."""

    # Overridden in the subclasses. Swaps the paths to the base lesson period
    # and to any substitutions depending on whether the query is run on a
    # lesson period or a substitution
    _period_path = None
    _subst_path = None

    def within_dates(self, start: date, end: date):
        """Filter for all lessons within a date range."""
        return self.filter(
            **{
                self._period_path + "lesson__validity__date_start__lte": start,
                self._period_path + "lesson__validity__date_end__gte": end,
            }
        )

    def in_week(self, wanted_week: CalendarWeek):
        """Filter for all lessons within a calendar week."""
        return self.within_dates(
            wanted_week[0] + timedelta(days=1) * (F(self._period_path + "period__weekday")),
            wanted_week[0] + timedelta(days=1) * (F(self._period_path + "period__weekday")),
        ).annotate_week(wanted_week)

    def on_day(self, day: date):
        """Filter for all lessons on a certain day."""
        week, weekday = week_weekday_from_date(day)

        return (
            self.within_dates(day, day)
            .filter(**{self._period_path + "period__weekday": weekday})
            .annotate_week(week)
        )

    def at_time(self, when: Optional[datetime] = None):
        """Filter for the lessons taking place at a certain point in time."""
        now = when or datetime.now()
        week, weekday = week_weekday_from_date(now.date())

        return self.filter(
            **{
                self._period_path + "lesson__validity__date_start__lte": now.date(),
                self._period_path + "lesson__validity__date_end__gte": now.date(),
                self._period_path + "period__weekday": now.weekday(),
                self._period_path + "period__time_start__lte": now.time(),
                self._period_path + "period__time_end__gte": now.time(),
            }
        ).annotate_week(week)

    def filter_participant(self, person: Union[Person, int]):
        """Filter for all lessons a participant (student) attends."""
        return self.filter(Q(**{self._period_path + "lesson__groups__members": person}))

    def filter_group(self, group: Union[Group, int]):
        """Filter for all lessons a group (class) regularly attends."""
        if isinstance(group, int):
            group = Group.objects.get(pk=group)

        if group.parent_groups.all():
            # Prevent to show lessons multiple times
            return self.filter(Q(**{self._period_path + "lesson__groups": group}))
        else:
            return self.filter(
                Q(**{self._period_path + "lesson__groups": group})
                | Q(**{self._period_path + "lesson__groups__parent_groups": group})
            )

    def filter_groups(self, groups: Iterable[Group]) -> QuerySet:
        """Filter for all lessons one of the groups regularly attends."""
        return self.filter(
            Q(**{self._period_path + "lesson__groups__in": groups})
            | Q(**{self._period_path + "lesson__groups__parent_groups__in": groups})
        )

    def filter_teacher(self, teacher: Union[Person, int], is_smart: bool = True):
        """Filter for all lessons given by a certain teacher."""
        qs1 = self.filter(**{self._period_path + "lesson__teachers": teacher})
        qs2 = self.filter(
            **{
                self._subst_path + "teachers": teacher,
                self._subst_path + "week": F("_week"),
                self._subst_path + "year": F("_year"),
            }
        )

        if is_smart:
            return qs1.union(qs2)
        else:
            return qs1

    def filter_room(self, room: Union["Room", int], is_smart: bool = True):
        """Filter for all lessons taking part in a certain room."""
        qs1 = self.filter(**{self._period_path + "room": room})
        qs2 = self.filter(
            **{
                self._subst_path + "room": room,
                self._subst_path + "week": F("_week"),
                self._subst_path + "year": F("_year"),
            }
        )

        if is_smart:
            return qs1.union(qs2)
        else:
            return qs1

    def filter_from_type(
        self, type_: TimetableType, obj: Union[Person, Group, "Room", int], is_smart: bool = True
    ) -> Optional[models.QuerySet]:
        """Filter lesson data for a group, teacher or room by provided type."""
        if type_ == TimetableType.GROUP:
            return self.filter_group(obj)
        elif type_ == TimetableType.TEACHER:
            return self.filter_teacher(obj, is_smart=is_smart)
        elif type_ == TimetableType.ROOM:
            return self.filter_room(obj, is_smart=is_smart)
        else:
            return None

    def filter_from_person(self, person: Person) -> Optional[models.QuerySet]:
        """Filter lesson data for a person."""
        type_ = person.timetable_type

        if type_ == TimetableType.TEACHER:
            # Teacher

            return self.filter_teacher(person)

        elif type_ == TimetableType.GROUP:
            # Student

            return self.filter_participant(person)

        else:
            # If no student or teacher
            return None

    def daily_lessons_for_person(
        self, person: Person, wanted_day: date
    ) -> Optional[models.QuerySet]:
        """Filter lesson data on a day by a person."""
        if person.timetable_type is None:
            return None

        lesson_periods = self.on_day(wanted_day).filter_from_person(person)

        return lesson_periods

    def group_by_validity(self) -> dict["ValidityRange", list["LessonPeriod"]]:
        """Group lesson periods by validity range as dictionary."""
        lesson_periods_by_validity = {}
        for lesson_period in self:
            lesson_periods_by_validity.setdefault(lesson_period.lesson.validity, [])
            lesson_periods_by_validity[lesson_period.lesson.validity].append(lesson_period)
        return lesson_periods_by_validity

    def next_lesson(
        self, reference: "LessonPeriod", offset: Optional[int] = 1
    ) -> Optional["LessonPeriod"]:
        """Get another lesson in an ordered set of lessons.

        By default, it returns the next lesson in the set. By passing the offset argument,
        the n-th next lesson can be selected. By passing a negative number, the n-th
        previous lesson can be selected.

        This function will handle week, year and validity range changes automatically
        if the queryset contains enough lesson data.
        """
        # Group lesson periods by validity to handle validity range changes correctly
        lesson_periods_by_validity = self.group_by_validity()
        validity_ranges = list(lesson_periods_by_validity.keys())

        # List with lesson periods in the validity range of the reference lesson period
        current_lesson_periods = lesson_periods_by_validity[reference.lesson.validity]
        pks = [lesson_period.pk for lesson_period in current_lesson_periods]

        # Position of the reference lesson period
        index = pks.index(reference.id)

        next_index = index + offset
        if next_index > len(pks) - 1:
            next_index %= len(pks)
            week = reference._week + 1
        elif next_index < 0:
            next_index = len(pks) + next_index
            week = reference._week - 1
        else:
            week = reference._week

        # Check if selected week makes a year change necessary
        year = reference._year
        if week < 1:
            year -= 1
            week = CalendarWeek.get_last_week_of_year(year).week
        elif week > CalendarWeek.get_last_week_of_year(year).week:
            year += 1
            week = 1

        # Get the next lesson period in this validity range and it's date
        # to check whether the validity range has to be changed
        week = CalendarWeek(week=week, year=year)
        next_lesson_period = current_lesson_periods[next_index]
        next_lesson_period_date = week_weekday_to_date(week, next_lesson_period.period.weekday)

        validity_index = validity_ranges.index(next_lesson_period.lesson.validity)

        # If date of next lesson period is out of validity range (smaller) ...
        if next_lesson_period_date < next_lesson_period.lesson.validity.date_start:
            # ... we have to get the lesson period from the previous validity range
            if validity_index == 0:
                # There are no validity ranges (and thus no lessons)
                # in the school term before this lesson period
                return None

            # Get new validity range and last lesson period of this validity range
            new_validity = validity_ranges[validity_index - 1]
            next_lesson_period = lesson_periods_by_validity[new_validity][-1]

            # Build new week with the date from the new validity range/lesson period
            week = CalendarWeek(
                week=new_validity.date_end.isocalendar()[1], year=new_validity.date_end.year
            )

        # If date of next lesson period is out of validity range (larger) ...
        elif next_lesson_period_date > next_lesson_period.lesson.validity.date_end:
            # ... we have to get the lesson period from the next validity range
            if validity_index >= len(validity_ranges) - 1:
                # There are no validity ranges (and thus no lessons)
                # in the school term after this lesson period
                return None

            # Get new validity range and first lesson period of this validity range
            new_validity = validity_ranges[validity_index + 1]
            next_lesson_period = lesson_periods_by_validity[new_validity][0]

            # Build new week with the date from the new validity range/lesson period
            week = CalendarWeek(
                week=new_validity.date_start.isocalendar()[1], year=new_validity.date_start.year
            )

        # Do a new query here to be able to annotate the new week
        return self.annotate_week(week).get(pk=next_lesson_period.pk)


class LessonPeriodQuerySet(LessonDataQuerySet, GroupByPeriodsMixin):
    """QuerySet with custom query methods for lesson periods."""

    _period_path = ""
    _subst_path = "substitutions__"


class LessonSubstitutionQuerySet(LessonDataQuerySet):
    """QuerySet with custom query methods for substitutions."""

    _period_path = "lesson_period__"
    _subst_path = ""

    def within_dates(self, start: date, end: date):
        """Filter for all substitutions within a date range."""
        start_week = CalendarWeek.from_date(start)
        end_week = CalendarWeek.from_date(end)
        return self.filter(
            week__gte=start_week.week,
            week__lte=end_week.week,
            year__gte=start_week.year,
            year__lte=end_week.year,
        ).filter(
            Q(
                week=start_week.week,
                year=start_week.year,
                lesson_period__period__weekday__gte=start.weekday(),
            )
            | Q(
                week=end_week.week,
                year=end_week.year,
                lesson_period__period__weekday__lte=end.weekday(),
            )
            | (
                ~Q(week=start_week.week, year=start_week.year)
                & ~Q(week=end_week.week, year=end_week.year)
            )
        )

    def in_week(self, wanted_week: CalendarWeek):
        """Filter for all lessons within a calendar week."""
        return self.filter(week=wanted_week.week, year=wanted_week.year).annotate_week(wanted_week)

    def on_day(self, day: date):
        """Filter for all lessons on a certain day."""
        week, weekday = week_weekday_from_date(day)

        return self.in_week(week).filter(lesson_period__period__weekday=weekday)

    def at_time(self, when: Optional[datetime] = None):
        """Filter for the lessons taking place at a certain point in time."""
        now = when or datetime.now()

        return self.on_day(now.date()).filter(
            lesson_period__period__time_start__lte=now.time(),
            lesson_period__period__time_end__gte=now.time(),
        )

    def affected_lessons(self):
        """Return all lessons which are affected by selected substitutions."""
        from .models import Lesson  # noaq

        return Lesson.objects.filter(lesson_periods__substitutions__in=self).distinct()

    def affected_teachers(self):
        """Get affected teachers.

        Return all teachers which are affected by
        selected substitutions (as substituted or substituting).
        """
        return (
            Person.objects.filter(
                Q(lessons_as_teacher__in=self.affected_lessons()) | Q(lesson_substitutions__in=self)
            )
            .distinct()
            .order_by("short_name")
        )

    def affected_groups(self):
        """Return all groups which are affected by selected substitutions."""
        return (
            Group.objects.filter(lessons__in=self.affected_lessons())
            .distinct()
            .order_by("short_name")
        )


class DateRangeQuerySetMixin:
    """QuerySet with custom query methods for models with date and period ranges.

    Filterable fields: date_start, date_end, period_from, period_to
    """

    def within_dates(self, start: date, end: date):
        """Filter for all events within a date range."""
        return self.filter(date_start__lte=end, date_end__gte=start)

    def in_week(self, wanted_week: CalendarWeek):
        """Filter for all events within a calendar week."""
        return self.within_dates(wanted_week[0], wanted_week[6])

    def on_day(self, day: date):
        """Filter for all events on a certain day."""
        return self.within_dates(day, day)

    def at_time(self, when: Optional[datetime] = None):
        """Filter for the events taking place at a certain point in time."""
        now = when or datetime.now()

        return self.on_day(now.date()).filter(
            period_from__time_start__lte=now.time(), period_to__time_end__gte=now.time()
        )

    def exclude_holidays(self, holidays: Iterable["Holiday"]) -> QuerySet:
        """Exclude all objects which are in the provided holidays."""
        q = Q()
        for holiday in holidays:
            q = q | Q(date_start__lte=holiday.date_end, date_end__gte=holiday.date_start)
        return self.exclude(q)


class AbsenceQuerySet(DateRangeQuerySetMixin, SchoolTermRelatedQuerySet):
    """QuerySet with custom query methods for absences."""

    def absent_teachers(self):
        return Person.objects.filter(absences__in=self).distinct().order_by("short_name")

    def absent_groups(self):
        return Group.objects.filter(absences__in=self).distinct().order_by("short_name")

    def absent_rooms(self):
        return Person.objects.filter(absences__in=self).distinct().order_by("short_name")


class HolidayQuerySet(QuerySet, DateRangeQuerySetMixin):
    """QuerySet with custom query methods for holidays."""

    def get_all_days(self) -> list[date]:
        """Get all days included in the selected holidays."""
        holiday_days = []
        for holiday in self:
            holiday_days += list(holiday.get_days())
        return holiday_days


class SupervisionQuerySet(ValidityRangeRelatedQuerySet, WeekQuerySetMixin):
    """QuerySet with custom query methods for supervisions."""

    def filter_by_weekday(self, weekday: int):
        """Filter supervisions by weekday."""
        return self.filter(
            Q(break_item__before_period__weekday=weekday)
            | Q(break_item__after_period__weekday=weekday)
        )

    def filter_by_teacher(self, teacher: Union[Person, int]):
        """Filter for all supervisions given by a certain teacher."""
        if self.count() > 0:
            if hasattr(self[0], "_week"):
                week = CalendarWeek(week=self[0]._week, year=self[0]._year)
            else:
                week = CalendarWeek.current_week()

            dates = [week[w] for w in range(0, 7)]

            return self.filter(
                Q(substitutions__teacher=teacher, substitutions__date__in=dates)
                | Q(teacher=teacher)
            )

        return self


class TimetableQuerySet(models.QuerySet):
    """Common query set methods for objects in timetables.

    Models need following fields:
    - groups
    - teachers
    - rooms (_multiple_rooms=True)/room (_multiple_rooms=False)
    """

    _multiple_rooms = True

    def filter_participant(self, person: Union[Person, int]):
        """Filter for all objects a participant (student) attends."""
        return self.filter(Q(groups__members=person))

    def filter_group(self, group: Union[Group, int]):
        """Filter for all objects a group (class) attends."""
        if isinstance(group, int):
            group = Group.objects.get(pk=group)

        if group.parent_groups.all():
            # Prevent to show lessons multiple times
            return self.filter(groups=group)
        else:
            return self.filter(Q(groups=group) | Q(groups__parent_groups=group))

    def filter_groups(self, groups: Iterable[Group]) -> QuerySet:
        """Filter for all objects one of the groups attends."""
        return self.filter(Q(groups__in=groups) | Q(groups__parent_groups__in=groups)).distinct()

    def filter_teacher(self, teacher: Union[Person, int]):
        """Filter for all lessons given by a certain teacher."""
        return self.filter(teachers=teacher)

    def filter_room(self, room: Union["Room", int]):
        """Filter for all objects taking part in a certain room."""
        if self._multiple_rooms:
            return self.filter(rooms=room)
        else:
            return self.filter(room=room)

    def filter_from_type(
        self, type_: TimetableType, obj: Union[Group, Person, "Room", int]
    ) -> Optional[models.QuerySet]:
        """Filter data for a group, teacher or room by provided type."""
        if type_ == TimetableType.GROUP:
            return self.filter_group(obj)
        elif type_ == TimetableType.TEACHER:
            return self.filter_teacher(obj)
        elif type_ == TimetableType.ROOM:
            return self.filter_room(obj)
        else:
            return None

    def filter_from_person(self, person: Person) -> Optional[models.QuerySet]:
        """Filter data by person."""
        type_ = person.timetable_type

        if type_ == TimetableType.TEACHER:
            # Teacher

            return self.filter_teacher(person)

        elif type_ == TimetableType.GROUP:
            # Student

            return self.filter_participant(person)

        else:
            # If no student or teacher
            return None


class EventQuerySet(DateRangeQuerySetMixin, SchoolTermRelatedQuerySet, TimetableQuerySet):
    """QuerySet with custom query methods for events."""

    def annotate_day(self, day: date):
        """Annotate all events in the QuerySet with the provided date."""
        return self.annotate(_date=models.Value(day, models.DateField()))

    def alias_day(self, day: date):
        """Add an alias to all events in the QuerySet with the provided date."""
        return self.alias(_date=models.Value(day, models.DateField()))


class ExtraLessonQuerySet(TimetableQuerySet, SchoolTermRelatedQuerySet, GroupByPeriodsMixin):
    """QuerySet with custom query methods for extra lessons."""

    _multiple_rooms = False

    def within_dates(self, start: date, end: date):
        """Filter all extra lessons within a specific time range."""
        return self.alias_day().filter(day__gte=start, day__lte=end)

    def on_day(self, day: date):
        """Filter all extra lessons on a day."""
        return self.within_dates(day, day)

    def _get_weekday_to_date(self):
        """Get DB function to convert a weekday to a date."""
        return ExpressionWrapper(
            Func(
                Concat(F("year"), F("week")),
                Value("IYYYIW"),
                output_field=DateField(),
                function="TO_DATE",
            )
            + F("period__weekday"),
            output_field=DateField(),
        )

    def annotate_day(self):
        return self.annotate(day=self._get_weekday_to_date())

    def alias_day(self):
        return self.alias(day=self._get_weekday_to_date())

    def exclude_holidays(self, holidays: Iterable["Holiday"]) -> QuerySet:
        """Exclude all extra lessons which are in the provided holidays."""
        q = Q()
        for holiday in holidays:
            q = q | Q(day__lte=holiday.date_end, day__gte=holiday.date_start)
        return self.alias_day().exclude(q)


class GroupPropertiesMixin:
    """Mixin for common group properties.

    Necessary method: `get_groups`
    """

    @property
    def group_names(self, sep: Optional[str] = ", ") -> str:
        return sep.join([group.short_name for group in self.get_groups()])

    @property
    def group_short_names(self, sep: Optional[str] = ", ") -> str:
        return sep.join([group.short_name for group in self.get_groups()])

    @property
    def groups_to_show(self) -> QuerySet[Group]:
        groups = self.get_groups()
        if (
            groups.count() == 1
            and groups[0].parent_groups.all()
            and get_site_preferences()["chronos__use_parent_groups"]
        ):
            return groups[0].parent_groups.all()
        else:
            return groups

    @property
    def groups_to_show_names(self, sep: Optional[str] = ", ") -> str:
        return sep.join([group.short_name for group in self.groups_to_show])

    @property
    def groups_to_show_short_names(self, sep: Optional[str] = ", ") -> str:
        return sep.join([group.short_name for group in self.groups_to_show])


class TeacherPropertiesMixin:
    """Mixin for common teacher properties.

    Necessary method: `get_teachers`
    """

    @property
    def teacher_names(self, sep: Optional[str] = ", ") -> str:
        return sep.join([teacher.full_name for teacher in self.get_teachers()])

    @property
    def teacher_short_names(self, sep: str = ", ") -> str:
        return sep.join([teacher.short_name for teacher in self.get_teachers()])


class RoomPropertiesMixin:
    """Mixin for common room properties.

    Necessary method: `get_rooms`
    """

    @property
    def room_names(self, sep: Optional[str] = ", ") -> str:
        return sep.join([room.name for room in self.get_rooms()])

    @property
    def room_short_names(self, sep: str = ", ") -> str:
        return sep.join([room.short_name for room in self.get_rooms()])


class LessonEventQuerySet(RecurrencePolymorphicQuerySet):
    """Queryset with special query methods for lesson events."""

    def for_teacher(self, teacher: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain person as teacher (including amends)."""
        amended = self.filter(Q(amended_by__isnull=False) & (Q(teachers=teacher))).values_list(
            "amended_by__pk", flat=True
        )
        return self.filter(Q(teachers=teacher) | Q(pk__in=amended)).distinct()

    def for_participant(self, person: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events the person participates in (including amends)."""
        amended = self.filter(Q(amended_by__isnull=False) & Q(groups__members=person)).values_list(
            "amended_by__pk", flat=True
        )
        return self.filter(Q(groups__members=person) | Q(pk__in=amended)).distinct()

    def for_group(self, group: Union[int, Group]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain group (including amends/as parent group)."""
        amended = self.filter(
            Q(amended_by__isnull=False) & (Q(groups=group) | Q(groups__parent_groups=group))
        ).values_list("amended_by__pk", flat=True)
        return self.filter(
            Q(groups=group) | Q(groups__parent_groups=group) | Q(pk__in=amended)
        ).distinct()

    def for_room(self, room: Union[int, Room]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain room (including amends)."""
        amended = self.filter(Q(amended_by__isnull=False) & (Q(rooms=room))).values_list(
            "amended_by__pk", flat=True
        )
        return self.filter(Q(rooms=room) | Q(pk__in=amended)).distinct()

    def for_course(self, course: Union[int, Course]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain course (including amends)."""
        amended = self.filter(Q(amended_by__isnull=False) & (Q(course=course))).values_list(
            "amended_by__pk", flat=True
        )
        return self.filter(Q(course=course) | Q(pk__in=amended)).distinct()

    def for_person(self, person: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain person (as teacher/participant, including amends)."""
        amended = self.filter(
            Q(amended_by__isnull=False) & (Q(teachers=person) | Q(groups__members=person))
        ).values_list("amended_by__pk", flat=True)
        return self.filter(
            Q(teachers=person) | Q(groups__members=person) | Q(pk__in=amended)
        ).distinct()

    def related_to_person(self, person: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events a certain person is allowed to see.

        This includes all lesson events the person is assigned to as
        teacher/participant/group owner/parent group owner,
        including those amended.
        """
        amended = self.filter(
            Q(amended_by__isnull=False)
            & (
                Q(teachers=person)
                | Q(groups__members=person)
                | Q(groups__owners=person)
                | Q(groups__parent_groups__owners=person)
            )
        ).values_list("amended_by__pk", flat=True)
        return self.filter(
            Q(teachers=person)
            | Q(groups__members=person)
            | Q(groups__owners=person)
            | Q(groups__parent_groups__owners=person)
            | Q(pk__in=amended)
        ).distinct()

    def not_amended(self) -> "LessonEventQuerySet":
        """Get all lesson events that are not amended."""
        return self.filter(amended_by__isnull=True)

    def not_amending(self) -> "LessonEventQuerySet":
        """Get all lesson events that are not amending other events."""
        return self.filter(amends__isnull=True)

    def amending(self) -> "LessonEventQuerySet":
        """Get all lesson events that are amending other events."""
        return self.filter(amends__isnull=False)


class SupervisionEventQuerySet(LessonEventQuerySet):
    pass
