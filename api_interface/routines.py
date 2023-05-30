from external import ApiSpbStuRuz


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
