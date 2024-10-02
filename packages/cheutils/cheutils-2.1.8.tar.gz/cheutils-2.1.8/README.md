# cheutils

A set of basic reusable utilities and tools to facilitate quickly getting up and going on any machine learning project.

### Features

- project_tree: methods for accessing the project tree - e.g., accessing the data and output folders, loading and savings Excel and CSV.
- common_utils: methods to support common programming tasks, such as labeling or tagging and date-stamping files
- propertiesutil: utility for managing properties files or project configuration, based on jproperties
- decorator_debug, decorator_timer, and decorator_singleton: decorators for enabling logging and method timers; as well as a singleton decorator

### Usage

```
import cheutils

# retrieve the path to the data folder, which is under the project root
get_data_dir()  # returns the path to the project data folder, which is always interpreted relative to the project root

# the following provide access to the properties file, usually expected to be named "app-config.properties" and typically found in the project data folder or anywhere either in the project root or any other subfolder
# You also have access to the LOGGER - you can simply call LOGGER.debug() in a similar way to you will when using loguru or standard logging
APP_PROPS = AppProperties()
LOGGER = LoguruWrapper().get_logger()

```
