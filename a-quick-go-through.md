## prerequisite

* Install az cli

  ```bash
  pip install azure-cli
  ```

* Install module cli from local feed (NOTE: The version will be updated after some bugfix)

  ```bash
  pip install keyring artifacts-keyring
  pip install --extra-index-url=https://msdata.pkgs.visualstudio.com/_packaging/azureml-modules%40Local/pypi/simple/ azureml-designer-tools==0.1.20.post11576103
  ```

* Prepare the environment

  ```bash
  # Login
  az login
  # Show account list, verify your default subscription
  az account list --output table
  # Set your default subscription if needed
  az account set -s "Your subscription name"
  # Configure workspace name and resource name
  az configure --defaults group="Your resource group name"
  az configure --defaults aml_workspace="Your workspace name"
  ```

  

* Register module

  ```bash
  # Register a module from local folder
  module register samples/sample_module_0.1.0
  # Register a module with newer version
  module register samples/sample_module_0.1.1
  # Register a module with a folder containing multiple module spec files
  module register samples/folder_with_multiple_module_specs --spec-file=add_rows.yaml
  ```

* List module

  ```bash
  module list --output table
  ```

* Module show detail

  ```bash
  module show "Sample Module"
  ```

* Module disable 

  ```bash
  module disable "Sample Module"
  module show "Sample Module" --output table
  ```

* Module enable

  ```bash
  module enable "Sample Module"
  module show "Sample Module" --output table
  ```

* Set as default version

  ```bash
  module set-default-version "Sample Module" --version 0.1.0
  module show "Sample Module" --output table
  ```

* Module download

  ```bash
  module download "Sample Module"
  ```

  