# Using the make_data.py script to generate more features

To add more features to the spotify data csv file, simply run the `make_data.py` script with no arguments. The 2 `.pkl` files in the project are important to maintain state of our data and the script checks for duplicates and avoids appending them. The running program can be terminated at any time and .pkl files will reflect the last entry added before halting. To actually add the data to the csv however, use the utility function in `utils.py` called `make_csv_from_features` and pass in the <i><b>unpickled</b></i> `features.pkl` structure as a single argument.

## Example

```python
# some_script.py
from utils import make_csv_from_features
import pandas as pd
features = pd.read_pickle("features.pkl")
df = make_csv_from_features(features) # after this call, spotify_data.csv is updated.
```

If you add new features, don't forget to push it!