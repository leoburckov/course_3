from dataclasses import dataclass


@dataclass
class Employer:
    """Модель работодателя"""
    id: int
    name: str
    url: str
    description: str = ""

    @classmethod
    def from_hh_data(cls, data: dict) -> 'Employer':
        return cls(
            id=data['id'],
            name=data['name'],
            url=data['alternate_url'],
            description=data.get('description', '')
        )