from credmark import Model


class Circle(Model):
    """
    This is the base class for all circle models. It's assumed that
    radius is the only needed input for all circle-related
    computation.
    """

    def get_result(self, radius):
        pass

    def run(self, input):

        result = {'value': 'ERROR, see logs.'}

        try:
            result = {'value': self.get_result(input['radius'])}
        except KeyError as err:
            self.logger.error('Required input parameter %s missing.' % err)

        return result
