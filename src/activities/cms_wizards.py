from cms.wizards.wizard_base import Wizard
from cms.wizards.wizard_pool import wizard_pool
from .forms import ActivityForm

class ActivityWizard(Wizard):
    pass


activity_wizard = ActivityWizard(
    title='New Activity',
    weight=200,
    form=ActivityForm,
    description='Create a new activity',
)

wizard_pool.register(activity_wizard)
