from global_obj.main import Global
# from core.mech.base.skills.details_manipulations import DisconnectDetailSkill


class SkillsPool:
    def __init__(self):
        self.skills = []
        self.id_to_skill: dict = {}
        # self.add_skill(DisconnectDetailSkill())

    def get_skill_by_id(self, unique_id):
        return self.id_to_skill.get(unique_id)

    def add_skill(self, skill):
        """
        :param skill: already initialized object
        """
        self.id_to_skill[skill.unique_id] = skill
        Global.logger.info(f'Added skill to skill pool: {skill.__dict__}')  # \n {self.id_to_skill}')

    def del_skill_by_id(self, unique_id):
        skill = self.id_to_skill.pop(unique_id, None)
        if skill is not None:
            self.skills.remove(skill)
