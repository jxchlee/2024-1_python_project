from pathlib import Path
import os
print(os.path.abspath('../../model/keras_model.h5'))
path = Path("../../model/keras_model.h5")
print(path.parent.absolute())