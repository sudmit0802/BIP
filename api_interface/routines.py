from .utils import *


async def get_teachers_routine():
    res = "teachers"
    async with ApiSpbStuRuz() as api:
        res = await api.get_teachers()
        ret = list()

        class Teacher():
            def __init__(self, tmp) -> None:
                self.id = tmp.id
                self.full_name = tmp.full_name
                self.chair = tmp.chair

        for building in res:
            elem = Teacher(building)
            if elem.chair:
                if elem.chair[0].isdigit() or elem.chair[0] == '?':
                    elem.chair = elem.chair[5:]
            ret.append(elem)

    return ret


async def get_faculties_routine():
    res = "faculties"
    async with ApiSpbStuRuz() as api:
        res = await api.get_faculties()
    return res


async def get_groups_on_faculties_by_id_routine(id):
    res = "groups"
    async with ApiSpbStuRuz() as api:
        res = await api.get_groups_on_faculties_by_id(id)
    return res


async def get_subjects_routine(group_id):
    res = "subjects"
    current_full_date = datetime.datetime.now()

    if current_full_date.month == 1:
        year = current_full_date.year - 1
        month = 10
    else:
        if current_full_date.month < 9:
            year = current_full_date.year
            month = 4
        else:
            year = current_full_date.year
            month = 10

    day = get_second_monday(year, month)

    async with ApiSpbStuRuz() as api:
        res1 = await api.get_groups_scheduler_by_id_and_date(group_id, year, month, day)
        res2 = await api.get_groups_scheduler_by_id_and_date(group_id, year, month, day + 7)

    res = list()
    for day in res1.days:
        for lesson in day.lessons:
            if lesson.subject not in res:
                res.append(lesson.subject)

    for day in res2.days:
        if lesson.subject not in res:
            res.append(lesson.subject)

    return res


async def get_buildings_routine():
    res = "buildings"
    async with ApiSpbStuRuz() as api:

        res = await api.get_buildings()
        ret = list()

        class Building():
            def __init__(self, tmp) -> None:
                self.id = tmp.id
                self.name = tmp.name
                self.abbr = tmp.abbr
                self.address = tmp.address

        for building in res:
            elem = Building(building)
            if not elem.address:
                elem.address = "Территория СПБПУ"
            ret.append(elem)

    return ret
