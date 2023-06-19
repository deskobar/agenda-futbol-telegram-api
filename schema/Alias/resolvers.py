from models import Alias


async def set_alias(user_id: str, team_name: str, alias: str):
    prev_alias = await Alias.objects.get_or_none(user_id=user_id, team_name=team_name)
    if prev_alias is None:
        await Alias.objects.create(user_id=user_id, team_name=team_name, alias=alias)
    else:
        prev_alias.team_name = team_name
        await prev_alias.save()
    return "Alias set successfully"


async def get_alias(user_id: str, team_name: str):
    prev_alias = await Alias.objects.get_or_none(user_id=user_id, team_name=team_name)
    if prev_alias is None:
        return "Alias not found"
    return prev_alias.alias
