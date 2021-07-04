class PlayerModel:
    def __init__(self, **kwargs):
        attr_dict = {val: 0 if val == 'player_id' else '' for val in ['playerId', 'nameUse', 'nameLast']}
        attr_dict.update(kwargs)

        for key, val in attr_dict.items():
            setattr(self, key, val)

        self._attr_dict = attr_dict

    def to_dict(self):
        return {
            key: val for key, val in self._attr_dict.items()
        }
