import strawberry


@strawberry.type
class Event:
    date: str
    match: str
    tournament: str
    hour: str
    channel: str

    @classmethod
    def from_entry(cls, entry) -> "Event":
        return Event(
            date=entry["FECHA"],
            match=entry["PARTIDO"],
            tournament=entry["COMPETENCIA"],
            hour=entry["HORARIO"],
            channel=entry["CANAL"],
        )
