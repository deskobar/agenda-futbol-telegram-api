from models import Alias


async def set_alias(user_id: str, team_name: str, alias: str) -> str:
    prev_alias = await Alias.objects.get_or_none(user_id=user_id, team_name=team_name)
    if prev_alias is None:
        await Alias.objects.create(user_id=user_id, team_name=team_name, alias=alias)
    else:
        prev_alias.alias = alias
        await prev_alias.update()
    return "Alias set successfully"


async def get_alias(user_id: str, team_name: str) -> str:
    prev_alias = await Alias.objects.get_or_none(user_id=user_id, team_name=team_name)
    if prev_alias is None:
        return "Alias not found"
    return prev_alias.alias
