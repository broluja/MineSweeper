from pydantic import BaseModel, Extra, Field


def snake_to_camel_case(value: str) -> str:
    """Refactoring snake case to camel case."""
    if not isinstance(value, str):
        raise ValueError('Please use a string object.')
    words = value.split('_')
    value = ''.join(word.title() for word in words if word)
    return f'{value[0].lower()}{value[1:]}'


class CustomBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = snake_to_camel_case
        allow_population_by_field_name = True


class Player(CustomBaseModel):
    """Player model."""
    player_name: str = Field(default='Player', alias='playerName')
    games_played: int = Field(default=0, alias='gamesPlayed')
    games_won: int = Field(default=0, alias='gamesWon')
