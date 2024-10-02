from .version import __version__, __versiondate__, __license__
from .settings      import *
from .utils         import *
from .arrays        import *
from .timepars      import *
from .parameters    import *
from .distributions import *
from .people        import *
from .modules       import *
from .networks      import *
from .results       import *
from .demographics  import *
from .products      import *
from .interventions import *
from .demographics  import *
from .disease       import *
from .diseases      import *
from .loop          import *
from .sim           import *
from .run           import *
from .calibration   import *
from .samples       import *

# Assign the root folder
import sciris as sc
root = sc.thispath(__file__).parent

# Import the version and print the license
if options.verbose:
    print(__license__)

# Double-check key requirements -- should match setup.py
reqs = ['sciris>=3.2.0', 'pandas>=2.0.0', 'scipy', 'numba', 'networkx']
msg = f'The following dependencies for Starsim {__version__} were not met: <MISSING>.'
sc.require(reqs, message=msg)
del sc, reqs, msg # Don't keep this in the module